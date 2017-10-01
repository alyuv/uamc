
class TelexRouter:
    app_label = 'meteodata'
    meteodata = 'meteodata'

    def db_for_read(self, model, **hints):
        """Point all operations on telex models to 'meteodata'"""
        if model._meta.app_label == self.app_label:
            return self.meteodata
        return 'default'

    def db_for_write(self, model, **hints):
        """Point all operations on telex models to 'meteodata'"""
        if model._meta.app_label == self.app_label:
            return self.meteodata
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """Allow any relation if a both models in telex app"""
        if obj1._meta.app_label == self.app_label and \
                        obj2._meta.app_label == self.app_label:
            return True
        # Allow if neither is telex app
        elif self.app_label not in [obj1._meta.app_label,
                                    obj2._meta.app_label]:
            return True
        return False

    def allow_syncdb(self, db, model):
        if db == self.meteodata or model._meta.app_label == self.app_label:
            return False  # we're not using syncdb on our legacy database
        else:  # but all other models/databases are fine
            return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == self.app_label:
            return self.meteodata
        return None

