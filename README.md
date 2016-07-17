MoLA
====

Modular's life assistant

# run unit tests
python -m unittest discover


# internationalize your app:
* mkdir -p i18n/fr/LC_MESSAGES
* xgettext --language=Python --keyword=_ --output=./i18n/<CLASS_NAME>.pot ./example.py
* msginit --input=./i18n/<CLASS_NAME>.pot --output=./i18n/fr/LC_MESSAGES/<CLASS_NAME>.po
* msgfmt ./i18n/fr/LC_MESSAGES/<CLASS_NAME>.po --output-file ./i18n/fr/LC_MESSAGES/<CLASS_NAME>.mo
* sudo cp ./i18n/fr/LC_MESSAGES/<CLASS_NAME>.mo /usr/share/locale/fr/LC_MESSAGES/<CLASS_NAME>.mo
