import uuid
import hashlib
import base64

class IdMapper:
    """
    Classe para mapear IDs internos da base de dados para IDs externos da API.
    Usa UUID v4 para gerar IDs únicos e seguros para exposição externa.
    """
    _instance = None
    _internal_to_external = {}
    _external_to_internal = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_external_id(self, internal_id: int, entity_type: str) -> str:
        """
        Converte um ID interno da BD para um ID externo da API.
        
        Args:
            internal_id: ID interno da base de dados
            entity_type: Tipo da entidade (ex: 'defense', 'vulnerability', 'attack', 'incident')
        
        Returns:
            ID externo (UUID string)
        """
        key = f"{entity_type}_{internal_id}"
        
        if key not in self._internal_to_external:
            # Gera um UUID baseado no tipo e ID interno para consistência
            # Usa hash para garantir que o mesmo ID interno sempre gere o mesmo UUID
            seed = f"{entity_type}_{internal_id}".encode()
            namespace = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')
            external_id = str(uuid.uuid5(namespace, seed.decode()))
            self._internal_to_external[key] = external_id
            self._external_to_internal[external_id] = internal_id
        
        return self._internal_to_external[key]

    def get_internal_id(self, external_id: str) -> int:
        """
        Converte um ID externo da API para um ID interno da BD.
        
        Args:
            external_id: ID externo (UUID string)
        
        Returns:
            ID interno da base de dados
        """
        return self._external_to_internal.get(external_id)

    def clear_mapping(self, external_id: str):
        """
        Remove um mapeamento quando uma entidade é deletada.
        """
        if external_id in self._external_to_internal:
            internal_id = self._external_to_internal[external_id]
            # Encontra e remove a chave correspondente
            for key, ext_id in list(self._internal_to_external.items()):
                if ext_id == external_id:
                    del self._internal_to_external[key]
                    break
            del self._external_to_internal[external_id]




