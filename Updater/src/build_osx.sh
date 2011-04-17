echo "### BUILDING PYONLINE UPDATE MANAGER###"

echo "Removing old setup_updatemanager.py"
rm setup_updatemanager.py > /dev/null

echo "Generating a new setup.py"
/Library/Frameworks/Python.framework/Versions/2.5/bin/py2applet --make-setup Update_Manager.py > /dev/null

#Rename setup.py
mv -f setup.py setup_updatemanager.py > /dev/null

echo "Removing old buld and dist data"
rm -rf build/ > /dev/null
rm -rf dist/ > /dev/null

echo "Building OSX Update_Manager.app... (may take some time)"
python2.5 setup_updatemanager.py py2app > /dev/null

echo "Moving compiled PyOnline Update Manager to Deploy directory"
mkdir Deploy > /dev/null
cp -rf dist/ Deploy > /dev/null

echo "### BUILDING PYONLINE UPDATE MANAGER COMPLETE###"
