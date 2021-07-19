from distutils.core import setup

import numpy as np
import os
from Cython.Build import cythonize

numpy_include = np.get_include()

abs_path = os.path.abspath(__file__)
abs_dir = os.path.dirname(abs_path)
print(abs_dir)
setup(ext_modules=cythonize(abs_dir + "/bbox.pyx"), include_dirs=[numpy_include])
setup(ext_modules=cythonize(abs_dir + "/nms.pyx"), include_dirs=[numpy_include])
