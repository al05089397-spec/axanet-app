import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class AxanetManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.clients_dir = os.path.join(data_dir, "clients")
        self.index_file = os.path.join(data_dir, "index.json")
        self._ensure_directories()
        
    def _ensure_directories(self):
        """Crea las carpetas necesarias si no existen"""
        os.makedirs(self.clients_dir, exist_ok=True)
        if not os.path.exists(self.index_file):
            self._save_index({})
    
    def _load_index(self) -> Dict[str, str]:
        """Carga el índice desde el archivo JSON"""
        try:
            with open(self.index_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_index(self, index: Dict[str, str]):
        """Guarda el índice al archivo JSON"""
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
    
    def _generate_filename(self, client_name: str) -> str:
        """Genera un nombre de archivo seguro basado en el nombre del cliente"""
        # Limpia caracteres especiales y espacios
        safe_name = "".join(c for c in client_name if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_name = safe_name.replace(' ', '_').lower()
        return f"{safe_name}.json"
    
    def _load_client_data(self, filename: str) -> Optional[Dict]:
        """Carga los datos de un cliente desde su archivo"""
        filepath = os.path.join(self.clients_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return None
    
    def _save_client_data(self, filename: str, client_data: Dict):
        """Guarda los datos de un cliente en su archivo"""
        filepath = os.path.join(self.clients_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(client_data, f, ensure_ascii=False, indent=2)
    
    def create_client(self, name: str, service: str, notes: str = "") -> bool:
        """
        Crea un nuevo cliente
        Returns: True si se creó exitosamente, False si ya existe
        """
        index = self._load_index()
        
        # Verificar si el cliente ya existe
        if name in index:
            return False
        
        # Generar nombre de archivo y crear datos del cliente
        filename = self._generate_filename(name)
        client_data = {
            "name": name,
            "service": service,
            "notes": notes,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "history": [
                {
                    "action": "created",
                    "service": service,
                    "notes": notes,
                    "timestamp": datetime.now().isoformat()
                }
            ]
        }
        
        # Guardar archivo del cliente y actualizar índice
        self._save_client_data(filename, client_data)
        index[name] = filename
        self._save_index(index)
        
        return True
    
    def update_client(self, name: str, service: str = None, notes: str = None) -> bool:
        """
        Actualiza un cliente existente
        Returns: True si se actualizó exitosamente, False si no existe
        """
        index = self._load_index()
        
        if name not in index:
            return False
        
        filename = index[name]
        client_data = self._load_client_data(filename)
        
        if not client_data:
            return False
        
        # Actualizar campos si se proporcionan
        updated = False
        if service is not None and service != client_data.get("service"):
            client_data["service"] = service
            updated = True
        
        if notes is not None and notes != client_data.get("notes"):
            client_data["notes"] = notes
            updated = True
        
        if updated:
            client_data["updated_at"] = datetime.now().isoformat()
            
            # Agregar entrada al historial
            history_entry = {
                "action": "updated",
                "timestamp": datetime.now().isoformat()
            }
            if service is not None:
                history_entry["service"] = service
            if notes is not None:
                history_entry["notes"] = notes
            
            client_data["history"].append(history_entry)
            
            # Guardar cambios
            self._save_client_data(filename, client_data)
        
        return True
    
    def consult_client(self, name: str) -> Optional[Dict]:
        """
        Consulta los datos de un cliente
        Returns: Datos del cliente o None si no existe
        """
        index = self._load_index()
        
        if name not in index:
            return None
        
        filename = index[name]
        client_data = self._load_client_data(filename)
        
        # Registrar la consulta en el historial
        if client_data:
            client_data["history"].append({
                "action": "consulted",
                "timestamp": datetime.now().isoformat()
            })
            self._save_client_data(filename, client_data)
        
        return client_data
    
    def list_clients(self) -> List[Dict]:
        """
        Lista todos los clientes con su información básica
        Returns: Lista de diccionarios con datos de clientes
        """
        index = self._load_index()
        clients = []
        
        for name, filename in index.items():
            client_data = self._load_client_data(filename)
            if client_data:
                # Solo incluir información básica para el listado
                clients.append({
                    "name": client_data["name"],
                    "service": client_data["service"],
                    "notes": client_data["notes"],
                    "created_at": client_data["created_at"],
                    "updated_at": client_data["updated_at"]
                })
        
        # Ordenar por fecha de creación (más recientes primero)
        clients.sort(key=lambda x: x["created_at"], reverse=True)
        return clients
    
    def delete_client(self, name: str) -> bool:
        """
        Elimina un cliente
        Returns: True si se eliminó exitosamente, False si no existe
        """
        index = self._load_index()
        
        if name not in index:
            return False
        
        filename = index[name]
        filepath = os.path.join(self.clients_dir, filename)
        
        # Eliminar archivo del cliente
        try:
            os.remove(filepath)
        except FileNotFoundError:
            pass  # El archivo ya no existe, continuar
        
        # Actualizar índice
        del index[name]
        self._save_index(index)
        
        return True
    
    def get_client_count(self) -> int:
        """Retorna el número total de clientes"""
        index = self._load_index()
        return len(index)
    
    def search_clients(self, query: str) -> List[Dict]:
        """
        Busca clientes por nombre, servicio o notas
        Returns: Lista de clientes que coinciden con la búsqueda
        """
        all_clients = self.list_clients()
        query_lower = query.lower()
        
        matching_clients = []
        for client in all_clients:
            if (query_lower in client["name"].lower() or 
                query_lower in client["service"].lower() or 
                query_lower in client["notes"].lower()):
                matching_clients.append(client)
        
        return matching_clients