CHANGELOG
=========

v0.4.4
------

- Performance: mark :code:`active`, :code:`found`, and :code:`inactive`
  properties on :code:`Finder` instances as :code:`cpdef`-ed methods, decreasing
  the Python-space operations for an increase in speed
- Performance: remove :code:`_Failed` exception and replace it with error codes,
  decreasing the Python-space operations for a speed increase
- Include :code:`Cython`-generated annotation file to keep an eye on the
  Python-interaction level

v0.4.3
------

- Performance: :code:`cdef` declare :code:`long` variable responsible for
  iterating over the buffer

v0.4.2
------

- Performance: avoid repeated function calls to check the buffer length

v0.4.1
------

- Add Sphinx documentation and make them available on
  https://streaming-form-data.readthedocs.org

v0.4.0
------

- Provide :code:`parser.register` function for handling uploaded parts,
  replacing the :code:`expected_parts` argument
- Remove :code:`Part` class from the user-facing API since it just makes the
  API look messy and verbose
- Update documentation

v0.3.2
------

- Include upload form in tornado usage example
- Call :code:`unset_active_part` when a delimiter string is found

v0.3.1
------

- Update README and tornado usage example
- Adjust import paths for the :code:`Part` class

v0.3.0
------

- Initial release
