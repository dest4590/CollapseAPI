class StatisticsRouter:
    """
    A router to control all database operations on models for the statistics app
    """

    route_app_labels = {"client_statistics"}

    def db_for_read(self, model, **hints):
        if model._meta.app_label == "client_statistics":
            return "statistics"
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == "client_statistics":
            return "statistics"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        db_set = {"default", "statistics"}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == "client_statistics":
            return db == "statistics"
        elif db == "statistics":
            return False
        return None
