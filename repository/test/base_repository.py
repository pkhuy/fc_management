from typing import Dict, List
from database import model
from database.test import mock_model

def insert(data) -> dict:
        """ Select Pet By pet_id """

        self.by_pet_id_param["pet_id"] = pet_id
        response = None
        validate_entry = isinstance(pet_id, int)

        if validate_entry:
            response = [mock_pet()]

        return {"Success": validate_entry, "Data": response}

def by_user_id(self, user_id: int) -> Dict[bool, List[Pets]]:
        """ Select Pet By user_id """

        self.by_user_id_param["user_id"] = user_id
        response = None
        validate_entry = isinstance(user_id, int)

        if validate_entry:
            response = [mock_pet()]

        return {"Success": validate_entry, "Data": response}

def by_pet_id_and_user_id(
        self, pet_id: int, user_id: int
    ) -> Dict[bool, List[Pets]]:
        """ Select Pet By user_id """

        self.by_pet_id_and_user_id_param["pet_id"] = pet_id
        self.by_pet_id_and_user_id_param["user_id"] = user_id
        response = None
        validate_entry = isinstance(user_id, int) and isinstance(pet_id, int)

        if validate_entry:
            response = [mock_pet()]

        return {"Success": validate_entry, "Data": response}
