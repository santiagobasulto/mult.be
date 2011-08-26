import inspect
from google.appengine.ext import db

#
#
#
# adds decorators that you can use on db.Model classes to define 
# callbacks methods for @before_put, @after_put, @before_delete, @after_delete
# 
# Chris Farmiloe 2011
#
#

HOOKS = {}
MODELS = {}

def itersubclasses(cls, _seen=None):
    "Generator over all subclasses of a given class, in depth first order"
    if _seen is None: _seen = set()
    subs = cls.__subclasses__()
    for sub in subs:
        if sub not in _seen:
            _seen.add(sub)
            yield sub
            for sub in itersubclasses(sub, _seen):
                yield sub

def find_model(kind_name):
    "looks up a model class by name"
    if kind_name not in MODELS:     
        for model in itersubclasses(db.Model):
            if model.__name__ == kind_name:
                MODELS[kind_name] = model
    return MODELS.get(kind_name)

def register_hook(kind_name,event_name,fun):
    if event_name not in HOOKS:
        HOOKS[event_name] = {}
    if kind_name not in HOOKS[event_name]:
        HOOKS[event_name][kind_name] = []
    HOOKS[event_name][kind_name].append(fun)

def normalize_entities(entities, event_name):
    if not isinstance(entities, (list, tuple)):
        entities = (entities,)
    return (e for e in entities)
        
def call_hooks(entities, event_name):
    for entity in normalize_entities(entities, event_name):
        for kind_name in HOOKS[event_name]:
            # check if this entity is instance of kind_name
            model = find_model(kind_name)
            if not isinstance(entity,model):
                continue
            # call function registered for this type
            for fun in HOOKS[event_name][kind_name]:
                fun(entity)

def patch_hooks(method, name):
    # Patches google.appengine.ext.db to add callbacks
    def hooked_fun(entities, **kwargs):
        call_hooks(entities,'before_%s' % name)
        a = method(entities, **kwargs)
        get_result = a.get_result
        def get_result_with_callback():
            call_hooks(entities,'after_%s' % name)
            return get_result()
        a.get_result = get_result_with_callback
        return a
    return hooked_fun
    
def hook(event_name):
    def new_decorator(fun):
        kind = inspect.getouterframes(inspect.currentframe())[1][3]
        register_hook(kind,event_name, fun)
        return fun
    return new_decorator

# create decorators
before_put    = hook('before_put')
after_put     = hook('after_put')
before_delete = hook('before_delete')
after_delete  = hook('after_delete')
    
# add patch
db.put_async    = patch_hooks(db.put_async,'put')
db.delete_async = patch_hooks(db.delete_async,'delete')



