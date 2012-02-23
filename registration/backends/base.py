class BackendBase(object):
    def register(self, username, email):
        pass

    def activate(self, activation_key, password=None):
        pass

    def accept(self, inspection_profile):
        pass

    def reject(self, inspection_profile):
        pass

    def get_activation_form(self):
        pass

    def get_registration_form(self):
        pass

    def get_rejection_profile(self, inspection_profile):
        pass

    def get_additional_profile(self, inspection_profile):
        pass
