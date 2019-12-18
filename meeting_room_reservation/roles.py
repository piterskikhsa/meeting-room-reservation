from rolepermissions.roles import AbstractUserRole


class Employee(AbstractUserRole):
    available_permissions = {
        'create_reservation': True,
    }


class OfficeManager(AbstractUserRole):
    available_permissions = {
        'confirm_reservation': True,
        'edit_meeting_room': True,
        'add_new_manager': True,
    }
