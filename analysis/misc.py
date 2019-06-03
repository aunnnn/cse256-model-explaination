import io
import pickle

class RenameUnpickler(pickle.Unpickler):
    """
    Load pickle with custom module path.
    Adapted from: https://stackoverflow.com/a/53327348/6666165

    Note 1: 
    ------
    When you save to pickle file, it basically remembers the module path of dependent objects in that environment.
    E.g., if you have `my_package.my_module` the time you save, 
    when it loads, it will find my_module exactly at `my_package.my_module`, regardless of where you put the my_module!

    This can be a problem if you use the pickle file in another project, where `my_package` doesn't exist. It's still looking for it.

    TL;DR: pickle is sensitive (at load-time) to the environment at save-time. This class handles that (nicely).
    """
    def find_class(self, module, name):
        renamed_module = module
        if module == "text_preprocessor":
            renamed_module = "analysis.text_preprocessor"

        return super(RenameUnpickler, self).find_class(renamed_module, name)

def renamed_load(file_obj):
    return RenameUnpickler(file_obj).load()