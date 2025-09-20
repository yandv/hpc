#!/usr/bin/env python3
"""
Script para testar performance dos algoritmos de ordenação
Testa algoritmos sequenciais e paralelos (merge e quick sort)
"""

import subprocess
import time
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import json

class PerformanceTester:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.out_dir = self.base_dir / "out"
        self.results = {}
        
        # Tamanhos de entrada para teste
        self.input_sizes = [1024*512, 1024*1024, 1024*1024*256, 1024*1024*512]
        
        # Números de threads para teste paralelo
        self.thread_counts = [1, 2, 4, 8, 16]
        
        # Algoritmos disponíveis
        self.algorithms = ["merge", "quick"]
        
        # Garantir que o diretório de saída existe
        self.out_dir.mkdir(exist_ok=True)
        
    def build_executables(self):
        """Compila os executáveis necessários"""
        print("Compilando executáveis...")

        try:
            result = subprocess.run(["make", "clean"], cwd=self.base_dir, 
                                  capture_output=True, text=True, check=True)
            result = subprocess.run(["make", "all"], cwd=self.base_dir, 
                                  capture_output=True, text=True, check=True)
            print("Compilação concluída com sucesso!")
        except subprocess.CalledProcessError as e:
            print(f"Erro na compilação: {e}")
            print(f"stdout: {e.stdout}")
            print(f"stderr: {e.stderr}")
            sys.exit(1)
    
    def generate_test_data(self, size, filename):
        """Gera dados de teste com tamanho especificado"""
        print(f"Gerando dados de teste: {size} elementos -> {filename}")
        try:
            result = subprocess.run([
                str(self.out_dir / "generate.exe"), 
                str(size), 
                str(filename)
            ], capture_output=True, text=True, check=True)
            print(f"  {result.stdout.strip()}")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao gerar dados: {e}")
            print(f"stderr: {e.stderr}")
            return False
        return True
    
    def run_sequential_test(self, algorithm, input_file, output_file):
        """Executa teste sequencial"""
        print(f"  Testando {algorithm} sequencial...")
        try:
            start_time = time.time()
            result = subprocess.run([
                str(self.out_dir / "sort.exe"),
                algorithm,
                str(input_file),
                str(output_file)
            ], capture_output=True, text=True, check=True)
            end_time = time.time()
            
            execution_time = end_time - start_time
            print(f"    Tempo: {execution_time:.4f}s")
            return execution_time
        except subprocess.CalledProcessError as e:
            print(f"    Erro na execução: {e}")
            print(f"    stderr: {e.stderr}")
            return None
    
    def run_parallel_test(self, algorithm, threads, input_file, output_file):
        """Executa teste paralelo"""
        print(f"  Testando {algorithm} paralelo com {threads} threads...")
        try:
            start_time = time.time()
            result = subprocess.run([
                str(self.out_dir / "sort_parallel.exe"),
                algorithm,
                str(threads),
                str(input_file),
                str(output_file)
            ], capture_output=True, text=True, check=True)
            end_time = time.time()
            
            execution_time = end_time - start_time
            print(f"    Tempo: {execution_time:.4f}s")
            return execution_time
        except subprocess.CalledProcessError as e:
            print(f"    Erro na execução: {e}")
            print(f"    stderr: {e.stderr}")
            return None
    
    def run_all_tests(self):
        """Executa todos os testes"""
        print("Iniciando testes de performance...")
        
        # Inicializar estrutura de resultados
        self.results = {
            'sequential': {alg: {} for alg in self.algorithms},
            'parallel': {alg: {str(threads): {} for threads in self.thread_counts} for alg in self.algorithms}
        }
        
        for size in self.input_sizes:
            print(f"\n=== Testando com {size:,} elementos ===")
            
            # Gerar dados de teste
            input_file = self.out_dir / f"test_data_{size}.bin"
            if not self.generate_test_data(size, input_file):
                continue
            
            # Testes sequenciais
            print("Executando testes sequenciais...")
            for algorithm in self.algorithms:
                output_file = self.out_dir / f"sequential_{algorithm}_{size}.bin"
                exec_time = self.run_sequential_test(algorithm, input_file, output_file)
                if exec_time is not None:
                    self.results['sequential'][algorithm][str(size)] = exec_time
            
            # Testes paralelos
            print("Executando testes paralelos...")
            for algorithm in self.algorithms:
                for threads in self.thread_counts:
                    output_file = self.out_dir / f"parallel_{algorithm}_{threads}t_{size}.bin"
                    exec_time = self.run_parallel_test(algorithm, threads, input_file, output_file)
                    if exec_time is not None:
                        self.results['parallel'][algorithm][str(threads)][str(size)] = exec_time
    
    def save_results(self):
        """Salva os resultados em arquivo JSON"""
        results_file = self.out_dir / "performance_results.json"
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\nResultados salvos em: {results_file}")
    
    def create_performance_plots(self):
        """Cria gráficos de performance"""
        print("\nGerando gráficos de performance...")
        
        # Configurar matplotlib
        plt.style.use('default')
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Performance dos Algoritmos de Ordenação', fontsize=16)
        
        # Converter tamanhos para lista para facilitar plotagem
        sizes = [int(s) for s in self.results['sequential']['merge'].keys()]
        sizes.sort()
        
        # 1. Performance sequencial por tamanho
        ax1 = axes[0, 0]
        for algorithm in self.algorithms:
            times = [self.results['sequential'][algorithm].get(str(s), 0) for s in sizes]
            ax1.plot(times, sizes, 'o-', label=f'{algorithm.capitalize()} Sequencial', linewidth=2, markersize=6)
        ax1.set_xlabel('Tempo de Execução (s)')
        ax1.set_ylabel('Tamanho da Entrada')
        ax1.set_title('Performance Sequencial')
        ax1.set_xscale('log')
        ax1.set_yscale('log')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Performance paralela - Merge Sort
        ax2 = axes[0, 1]
        for threads in self.thread_counts:
            times = [self.results['parallel']['merge'].get(str(threads), {}).get(str(s), 0) for s in sizes]
            if any(times):  # Só plotar se houver dados
                ax2.plot(times, sizes, 'o-', label=f'{threads} threads', linewidth=2, markersize=6)
        ax2.set_xlabel('Tempo de Execução (s)')
        ax2.set_ylabel('Tamanho da Entrada')
        ax2.set_title('Merge Sort Paralelo')
        ax2.set_xscale('log')
        ax2.set_yscale('log')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Performance paralela - Quick Sort
        ax3 = axes[1, 0]
        for threads in self.thread_counts:
            times = [self.results['parallel']['quick'].get(str(threads), {}).get(str(s), 0) for s in sizes]
            if any(times):  # Só plotar se houver dados
                ax3.plot(times, sizes, 'o-', label=f'{threads} threads', linewidth=2, markersize=6)
        ax3.set_xlabel('Tempo de Execução (s)')
        ax3.set_ylabel('Tamanho da Entrada')
        ax3.set_title('Quick Sort Paralelo')
        ax3.set_xscale('log')
        ax3.set_yscale('log')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 4. Speedup por número de threads (para o maior tamanho)
        ax4 = axes[1, 1]
        if sizes:
            max_size = max(sizes)
            for algorithm in self.algorithms:
                # Tempo sequencial como baseline
                seq_time = self.results['sequential'][algorithm].get(str(max_size), 0)
                if seq_time > 0:
                    speedups = []
                    thread_list = []
                    for threads in self.thread_counts:
                        par_time = self.results['parallel'][algorithm].get(str(threads), {}).get(str(max_size), 0)
                        if par_time > 0:
                            speedup = seq_time / par_time
                            speedups.append(speedup)
                            thread_list.append(threads)
                    
                    if speedups:
                        ax4.plot(speedups, thread_list, 'o-', label=f'{algorithm.capitalize()} Sort', 
                                linewidth=2, markersize=6)
        
        ax4.set_xlabel('Speedup')
        ax4.set_ylabel('Número de Threads')
        ax4.set_title(f'Speedup vs Threads (n={max_size:,})')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Salvar gráfico na pasta out
        plot_file = self.out_dir / "performance_plots.png"
        plt.savefig(plot_file, dpi=300, bbox_inches='tight')
        print(f"Gráficos salvos em: {plot_file}")
        
        # Mostrar gráfico
        plt.show()
    
    def print_summary(self):
        """Imprime resumo dos resultados"""
        print("\n" + "="*60)
        print("RESUMO DOS RESULTADOS")
        print("="*60)
        
        # Performance sequencial
        print("\nPERFORMANCE SEQUENCIAL:")
        for algorithm in self.algorithms:
            print(f"\n{algorithm.capitalize()} Sort:")
            for size in sorted(self.results['sequential'][algorithm].keys(), key=int):
                time_val = self.results['sequential'][algorithm][size]
                print(f"  {int(size):,} elementos: {time_val:.4f}s")
        
        # Performance paralela
        print("\nPERFORMANCE PARALELA:")
        for algorithm in self.algorithms:
            print(f"\n{algorithm.capitalize()} Sort:")
            for threads in self.thread_counts:
                print(f"  {threads} threads:")
                for size in sorted(self.results['parallel'][algorithm][str(threads)].keys(), key=int):
                    time_val = self.results['parallel'][algorithm][str(threads)][size]
                    print(f"    {int(size):,} elementos: {time_val:.4f}s")
    
    def run(self):
        """Executa todo o processo de teste"""
        print("Iniciando testes de performance dos algoritmos de ordenação")
        print("="*60)
        
        # Compilar executáveis
        self.build_executables()
        
        # Executar testes
        self.run_all_tests()
        
        # Salvar resultados
        self.save_results()
        
        # Gerar gráficos
        self.create_performance_plots()
        
        # Imprimir resumo
        self.print_summary()
        
        print("\nTestes concluídos!")

def main():
    """Função principal"""
    tester = PerformanceTester()
    tester.run()

if __name__ == "__main__":
    main()
