#Sistema de Gestao de Tarefas Academicas

from datetime import datetime

tarefas = []
id_counter = 1

def validar_data(txt):
    try: return datetime.strptime(txt, "%d/%m/%Y")
    except: return None

def dias_restantes(data):
    return (data - datetime.now()).days

def cadastrar():
    global id_counter
    print("\n--- CADASTRAR TAREFA ---")
    t = input("Titulo: "); d = input("Descricao: "); disc = input("Disciplina: ")
    print("Prioridade: 1-Baixa 2-Media 3-Alta 4-Urgente"); p = int(input("Escolha: "))
    while True:
        dt = validar_data(input("Data (DD/MM/AAAA): "))
        if dt: break
        print("Data invalida!")
    tarefas.append({'id': id_counter, 'titulo': t, 'desc': d, 'disciplina': disc, 'prioridade': p, 'data': dt, 'ok': False})
    id_counter += 1
    print("Tarefa cadastrada com sucesso!")

def listar():
    print("\n--- LISTA DE TAREFAS ---")
    if not tarefas: print("Nenhuma tarefa cadastrada."); return
    pri = {1:"Baixa", 2:"Media", 3:"Alta", 4:"Urgente"}
    for t in tarefas:
        s = "Concluida" if t['ok'] else "Pendente"
        print(f"\nID: {t['id']} | {t['titulo']} | {t['disciplina']}")
        print(f"Prioridade: {pri[t['prioridade']]} | Status: {s} | Prazo: {dias_restantes(t['data'])} dias")

def atualizar():
    print("\n--- ATUALIZAR TAREFA ---")
    if not tarefas: 
        print("Nenhuma tarefa cadastrada."); return
    for t in tarefas: 
        print(f"ID {t['id']}: {t['titulo']}")
    
    id_b = int(input("Digite o ID: "))
    for t in tarefas:
        if t['id'] == id_b:
            print("1-Titulo 2-Prioridade 3-Marcar como concluida"); op = input("Escolha: ")
            if op == "1": t['titulo'] = input("Novo titulo: ")
            elif op == "2": t['prioridade'] = int(input("Nova prioridade (1-4): "))
            elif op == "3": t['ok'] = True
            print("Tarefa atualizada!"); return
    print("Tarefa nao encontrada!")

def excluir():
    print("\n--- EXCLUIR TAREFA ---")
    if not tarefas: print("Nenhuma tarefa cadastrada."); return
    
    for t in tarefas: print(f"ID {t['id']}: {t['titulo']}")
    id_b = int(input("Digite o ID: "))
    for t in tarefas:
        if t['id'] == id_b:
            if input(f"Confirma exclusao de '{t['titulo']}'? (S/N): ").upper() == 'S':
                tarefas.remove(t); print("Tarefa excluida!")
            return
    print("Tarefa nao encontrada!")

def atrasadas():
    print("\n--- TAREFAS ATRASADAS ---")
    atr = [t for t in tarefas if dias_restantes(t['data']) < 0 and not t['ok']]
    if not atr: print("Nenhuma tarefa atrasada."); return
    for t in atr: print(f"- {t['titulo']} ({t['disciplina']}) - Atrasada ha {abs(dias_restantes(t['data']))} dias")

def proximas():
    print("\n--- PROXIMAS ENTREGAS (7 DIAS) ---")
    prox = [t for t in tarefas if 0 <= dias_restantes(t['data']) <= 7 and not t['ok']]
    if not prox: print("Nenhuma entrega proxima."); return
    for t in prox: print(f"- {t['titulo']} ({t['disciplina']}) - Faltam {dias_restantes(t['data'])} dias")

def por_prioridade():
    print("\n--- TAREFAS POR PRIORIDADE ---")
    pri = {1:"Baixa", 2:"Media", 3:"Alta", 4:"Urgente"}
    for n in [4,3,2,1]:
        print(f"\nPrioridade {pri[n]}:")
        lista = [t for t in tarefas if t['prioridade'] == n and not t['ok']]
        if lista: [print(f"  - {t['titulo']}") for t in lista]
        else: print("  (nenhuma tarefa)")

def stats():
    print("\n--- ESTATISTICAS GERAIS ---")
    if not tarefas: print("Nenhuma tarefa cadastrada."); return
    total = len(tarefas)
    conc = len([t for t in tarefas if t['ok']])
    atr = len([t for t in tarefas if dias_restantes(t['data']) < 0 and not t['ok']])
    print(f"Total de tarefas: {total}")
    print(f"Concluidas: {conc} ({conc*100//total}%)")
    print(f"Pendentes: {total-conc}")
    print(f"Atrasadas: {atr}")

def menu_relatorios():
    while True:
        print("\n--- MENU DE RELATORIOS ---")
        print("1 - Tarefas Atrasadas")
        print("2 - Proximas Entregas")
        print("3 - Agrupar por Prioridade")
        print("4 - Estatisticas Gerais")
        print("0 - Voltar ao Menu Principal")
        op = input("Escolha uma opcao: ")
        if op == "1": atrasadas()
        elif op == "2": proximas()
        elif op == "3": por_prioridade()
        elif op == "4": stats()
        elif op == "0": break

def main():
    while True:
        print("\n" + "="*45)
        print("SISTEMA DE GESTAO DE TAREFAS ACADEMICAS")
        print("="*45)
        print("1 - Cadastrar Nova Tarefa")
        print("2 - Listar Todas as Tarefas")
        print("3 - Atualizar Tarefa")
        print("4 - Excluir Tarefa")
        print("5 - Relatorios e Analises")
        print("0 - Sair do Sistema")
        op = input("Escolha uma opcao: ")
        if op == "1": cadastrar()
        elif op == "2": listar()
        elif op == "3": atualizar()
        elif op == "4": excluir()
        elif op == "5": menu_relatorios()
        elif op == "0": print("\nObrigado por usar o sistema. Ate logo!"); break

if __name__ == "__main__": main()