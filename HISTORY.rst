=======
History
=======

0.1.0 (2019-03-29)
------------------

* First release on PyPI.

0.1.4 (2019-05-11)
------------------

* Multiple bug fixes
* Accepts Numpy arrays
* State factor for easy creation of material states
* State can now be set when initializing
* Expanded the base material properties
* Added support for Jupyter Markdown, LaTeX and HTML representation

0.2.0 (2019-05-25)
------------------

* Removed the need for a metaclass
* Observer pattern implemented as Chainable class
* Guarded descriptor added
* Modular materials, allows for mix and match of different models
* Two-domain-Tait-pvt added
* Cross-Arrhenius model added

0.2.1 (2019-05-25)
------------------

* property models, functions and values are cited by source

0.2.2 (2019-05-31)
------------------

* Couple of bug-fixes
* dir shows only user variables
* Interpolated function added (measurement data, can now be used)
* Serialization using dill is now possible
* repr string simplified
* Cross-WLF model added
* Some example materials added: PLA, PLA-TPU, PLA-TPS
