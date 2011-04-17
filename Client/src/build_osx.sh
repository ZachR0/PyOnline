echo "### BUILDING PYONLINE ###"

echo "Removing old setup_pyonline.py"
rm setup_pyonline.py > /dev/null

echo "Generating a new setup.py"
/Library/Frameworks/Python.framework/Versions/2.5/bin/py2applet --make-setup PyOnline.py > /dev/null

#Rename setup.py
mv -f setup.py setup_pyonline.py > /dev/null

echo "Removing old buld and dist data"
rm -rf build/ > /dev/null
rm -rf dist/ > /dev/null

echo "Building OSX PyOnline.app... (may take some time)"
python2.5 setup_pyonline.py py2app > /dev/null

echo "Copying data folder to PyOnline.app resources... (may take some time)"
cp -rf data/ dist/PyOnline.app/Contents/Resources/data > /dev/null

echo "Moving compiled PyOnline to Deploy directory"
rm -rf Deploy/osx > /dev/null
mkdir Deploy/osx > /dev/null
cp -rf dist/ Deploy/osx > /dev/null


echo "### BUILDING PYONLINE COMPLETE###"