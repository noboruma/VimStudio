import os
import glob
import fnmatch

class ProjectController:

    ANDROID_MANIFEST_FILE = 'AndroidManifest.xml'
    GRADLE_BUILD_FILE = "build.gradle"

    def fileExistsInCwd(self, filename, maxDepth):
        current_directory = os.getcwd()
        return self.fileExistsInDir(filename, current_directory, maxDepth)

    def fileExistsInDir(self, filename, directory, maxDepth):
        top = directory
        matches = self.fileNamesRetrieve(top, maxDepth, filename)

        if len(matches) > 0:
            return True
        else:
            return False

    def retrieveListOfEmulators(self):
        emulators = []
        emulatorDir = os.path.expanduser("~") + "/.android/avd"
        if os.path.isdir(emulatorDir):
            emulatorPaths = self.fileNamesRetrieve(emulatorDir, 1, "*.avd")
            for emulator in emulatorPaths:
                emulator = emulator.split("/")[-1]
                emulator = emulator[:-4]
                emulators.append(emulator)
        return emulators

    def fileNamesRetrieve(self, top, maxDepth, fnMask):
        someFiles = []

        for d in range(1, maxDepth+1):
            maxGlob = "/".join("*" * d)
            topGlob = os.path.join(top, maxGlob)
            allFiles = glob.glob(topGlob)

            someFiles.extend([f for f in allFiles if fnmatch.fnmatch(os.path.basename(f), fnMask )])

        for d in range(1, maxDepth+1):
            maxGlob = ".*".join("/" * (d + 1))[1:-1]
            topGlob = os.path.join(top, maxGlob)
            allFiles = glob.glob(topGlob)

            someFiles.extend([f for f in allFiles if fnmatch.fnmatch(os.path.basename(f), fnMask )])
        return someFiles

    def findFile(self, directory, name):
        matches = []
        for root, dirnames, filenames in os.walk(directory):
            for filename in fnmatch.filter(filenames, name):
                matches.append(os.path.join(root, filename))
        return matches

    def findDir(self, directory, name):
        matches = []
        for root, dirnames, filenames in os.walk(directory):
            for dirname in fnmatch.filter(dirnames, name):
                matches.append(os.path.join(root, dirname))
        return matches

    def isGradleProject(self):
        return self.fileExistsInCwd(self.GRADLE_BUILD_FILE, 1)

    def isAndroidProject(self):
        return self.fileExistsInCwd(self.ANDROID_MANIFEST_FILE, 10)

    def isBuilt(self):
        return bool(self.findDir(os.getcwd(), "build"))

    def findAndroidManifest(self):
        cwd = os.getcwd()
        manifest = self.ANDROID_MANIFEST_FILE
        arrayOfManifests = self.findFile(cwd, manifest)
        if arrayOfManifests:
            return arrayOfManifests.pop()
