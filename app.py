#!/usr/bin/env python3
"""
Axanet - Gestor de Clientes CLI
Aplicación para gestionar clientes con integración Git y GitHub Actions
"""

import argparse
import subprocess
import sys
from datetime import datetime
from axanet_manager import AxanetManager

class AxanetCLI:
    def __init__(self):
        self.manager = AxanetManager()
    
    def _git_operations(self, action: str, client_name: str, use_git: bool, push: bool):
        """Ejecuta operaciones Git si están habilitadas"""
        if not use_git:
            return
        
        try:
            # git add
            subprocess.run(['git', 'add', '.'], check=True, capture_output=True)
            
            # git commit con etiqueta específica para Actions
            commit_msg = f"[{action}] name={client_name}"
            subprocess.run(['git', 'commit', '-m', commit_msg], check=True, capture_output=True)
            
            print(f"✅ Commit realizado: {commit_msg}")
            
            if push:
                # git push
                subprocess.run(['git', 'push', 'origin', 'main'], check=True, capture_output=True)
                print("✅ Push exitoso a GitHub")
                
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Error en operación Git: {e}")
            print("Tip: Verifica que tengas un repo Git configurado y permisos para push")
    
    def create_client(self, args):
        """Crear nuevo cliente"""
        if self.manager.create_client(args.name, args.service, args.notes or ""):
            print(f"✅ Cliente '{args.name}' creado exitosamente")
            print(f"   Servicio: {args.service}")
            if args.notes:
                print(f"   Notas: {args.notes}")
            
            self._git_operations("NEW_CLIENT", args.name, args.git, args.push)
        else:
            print(f"❌ El cliente '{args.name}' ya existe")
            return 1
    
    def update_client(self, args):
        """Actualizar cliente existente"""
        if self.manager.update_client(args.name, args.service, args.notes):
            print(f"✅ Cliente '{args.name}' actualizado exitosamente")
            if args.service:
                print(f"   Nuevo servicio: {args.service}")
            if args.notes:
                print(f"   Nuevas notas: {args.notes}")
            
            self._git_operations("UPDATE_CLIENT", args.name, args.git, args.push)
        else:
            print(f"❌ El cliente '{args.name}' no existe")
            return 1
    
    def consult_client(self, args):
        """Consultar información de cliente"""
        client_data = self.manager.consult_client(args.name)
        
        if client_data:
            print(f"\n📋 Información de '{client_data['name']}':")
            print(f"   Servicio: {client_data['service']}")
            print(f"   Notas: {client_data['notes']}")
            print(f"   Creado: {self._format_datetime(client_data['created_at'])}")
            print(f"   Actualizado: {self._format_datetime(client_data['updated_at'])}")
            
            if len(client_data['history']) > 1:
                print(f"\n📈 Historial reciente:")
                for entry in client_data['history'][-3:]:  # Últimas 3 entradas
                    timestamp = self._format_datetime(entry['timestamp'])
                    action = entry['action']
                    print(f"   • {action.capitalize()} - {timestamp}")
            
            self._git_operations("CONSULT_CLIENT", args.name, args.git, args.push)
        else:
            print(f"❌ El cliente '{args.name}' no existe")
            return 1
    
    def list_clients(self, args):
        """Listar todos los clientes"""
        clients = self.manager.list_clients()
        
        if not clients:
            print("📭 No hay clientes registrados")
            return
        
        print(f"\n📊 Lista de clientes ({len(clients)} total):")
        print("-" * 80)
        
        for i, client in enumerate(clients, 1):
            print(f"{i:2}. {client['name']}")
            print(f"     Servicio: {client['service']}")
            if client['notes']:
                print(f"     Notas: {client['notes']}")
            print(f"     Actualizado: {self._format_datetime(client['updated_at'])}")
            if i < len(clients):
                print()
    
    def delete_client(self, args):
        """Eliminar cliente"""
        if not args.confirm:
            response = input(f"⚠️  ¿Estás seguro de eliminar al cliente '{args.name}'? (s/N): ")
            if response.lower() not in ['s', 'si', 'sí', 'y', 'yes']:
                print("❌ Operación cancelada")
                return 0
        
        if self.manager.delete_client(args.name):
            print(f"✅ Cliente '{args.name}' eliminado exitosamente")
            self._git_operations("DELETE_CLIENT", args.name, args.git, args.push)
        else:
            print(f"❌ El cliente '{args.name}' no existe")
            return 1
    
    def search_clients(self, args):
        """Buscar clientes"""
        results = self.manager.search_clients(args.query)
        
        if not results:
            print(f"🔍 No se encontraron clientes con '{args.query}'")
            return
        
        print(f"🔍 Resultados para '{args.query}' ({len(results)} encontrados):")
        print("-" * 60)
        
        for client in results:
            print(f"• {client['name']}")
            print(f"  Servicio: {client['service']}")
            if client['notes']:
                print(f"  Notas: {client['notes']}")
            print()
    
    def show_stats(self, args):
        """Mostrar estadísticas"""
        total = self.manager.get_client_count()
        print(f"\n📈 Estadísticas de Axanet:")
        print(f"   Total de clientes: {total}")
        
        if total > 0:
            recent_clients = self.manager.list_clients()[:5]
            print(f"\n🕒 Clientes más recientes:")
            for client in recent_clients:
                print(f"   • {client['name']} - {client['service']}")
    
    def _format_datetime(self, iso_string: str) -> str:
        """Formatea fecha ISO a formato legible"""
        try:
            dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d %H:%M')
        except:
            return iso_string
    
    def run(self):
        """Ejecutar la aplicación CLI"""
        parser = argparse.ArgumentParser(
            description="Axanet - Gestor de Clientes",
            epilog="Ejemplo: python app.py create --name 'Juan Pérez' --service 'Soldadura' --notes 'Cliente premium'"
        )
        
        # Argumentos globales
        parser.add_argument('--git', action='store_true', 
                          help='Hacer commit automático con etiqueta para GitHub Actions')
        parser.add_argument('--push', action='store_true',
                          help='Hacer push después del commit (requiere --git)')
        
        # Subcomandos
        subparsers = parser.add_subparsers(dest='command', help='Comandos disponibles')
        
        # Crear cliente
        create_parser = subparsers.add_parser('create', help='Crear nuevo cliente')
        create_parser.add_argument('--name', required=True, help='Nombre del cliente')
        create_parser.add_argument('--service', required=True, help='Servicio contratado')
        create_parser.add_argument('--notes', help='Notas adicionales')
        
        # Actualizar cliente
        update_parser = subparsers.add_parser('update', help='Actualizar cliente existente')
        update_parser.add_argument('--name', required=True, help='Nombre del cliente')
        update_parser.add_argument('--service', help='Nuevo servicio')
        update_parser.add_argument('--notes', help='Nuevas notas')
        
        # Consultar cliente
        consult_parser = subparsers.add_parser('consult', help='Consultar información de cliente')
        consult_parser.add_argument('--name', required=True, help='Nombre del cliente')
        
        # Listar clientes
        list_parser = subparsers.add_parser('list', help='Listar todos los clientes')
        
        # Eliminar cliente
        delete_parser = subparsers.add_parser('delete', help='Eliminar cliente')
        delete_parser.add_argument('--name', required=True, help='Nombre del cliente')
        delete_parser.add_argument('--confirm', action='store_true', help='Confirmar eliminación sin preguntar')
        
        # Buscar clientes
        search_parser = subparsers.add_parser('search', help='Buscar clientes por texto')
        search_parser.add_argument('--query', required=True, help='Texto a buscar')
        
        # Estadísticas
        stats_parser = subparsers.add_parser('stats', help='Mostrar estadísticas')
        
        # Parsear argumentos
        args = parser.parse_args()
        
        if not args.command:
            parser.print_help()
            return 1
        
        # Validar --push requiere --git
        if args.push and not args.git:
            print("❌ Error: --push requiere --git")
            return 1
        
        # Ejecutar comando correspondiente
        command_map = {
            'create': self.create_client,
            'update': self.update_client,
            'consult': self.consult_client,
            'list': self.list_clients,
            'delete': self.delete_client,
            'search': self.search_clients,
            'stats': self.show_stats
        }
        
        try:
            result = command_map[args.command](args)
            return result or 0
        except KeyboardInterrupt:
            print("\n❌ Operación cancelada por el usuario")
            return 1
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return 1

def main():
    """Función principal"""
    cli = AxanetCLI()
    return cli.run()

if __name__ == "__main__":
    sys.exit(main())