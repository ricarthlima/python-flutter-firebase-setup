def concatAll(list, divider):
    ret = ""
    for s in list:
        ret = ret + divider +  s
    return ret

import os

print("Selecione as dependências a serem instaladas (separadas por espaço):")
print("a - Todos\n0 - Authentication\n1 - Cloud Firestore\n2 - Storage\n3 - Push Notification\n4 - Analytics")

data = input()
data = data.split(" ")

# Get Package Name
fileAndroidManifest = open("android/app/src/main/AndroidManifest.xml", "r")
androidManifest = fileAndroidManifest.read()
packageName = androidManifest.split("package=")[1].split("\"")[1]
fileAndroidManifest.close()

print("Gere o arquivo google-services.json usando o seguinte nome do pacote:")
print(packageName)
print("Adicione o arquivo na raiz do projeto Flutter e pressione qualquer tecla")

# Move google-services.json
input()
os.replace("google-services.json", "android/google-services.json")

# Build Gradle in Project
fileGradleProject = open("android/build.gradle", "r")
gradleProject = fileGradleProject.read()
dependeceIndex = gradleProject.find("dependencies {") + len("dependencies {")

dependecies = ["classpath 'com.google.gms:google-services:4.3.10'"]

gradleProject = gradleProject[:dependeceIndex] + "\n" + concatAll(dependecies, '\n\t\t') + gradleProject[dependeceIndex:]

fileGradleProject.close()
fileGradleProject = open("android/build.gradle", "w")
fileGradleProject.write(gradleProject)
fileGradleProject.close()

# Build Gradle in App
fileGradleApp = open("android/app/build.gradle", "r")
gradleApp = fileGradleApp.read()

pluginsIndex = gradleApp.find('flutter.gradle"') + len('flutter.gradle"')
plugins = ["apply plugin: 'com.google.gms.google-services'"]
gradleApp = gradleApp[:pluginsIndex] + concatAll(plugins, '\n') + gradleApp[pluginsIndex:]


dependecies = ["implementation platform('com.google.firebase:firebase-bom:29.0.0')","implementation 'com.google.firebase:firebase-analytics'"]
dependeceIndex = gradleApp.find("dependencies {") + len("dependencies {")
gradleApp = gradleApp[:dependeceIndex] + concatAll(dependecies, '\n\t') + gradleApp[dependeceIndex:]

# print(gradleApp)
fileGradleApp.close()
fileGradleApp = open("android/app/build.gradle", "w")
fileGradleApp.write(gradleApp)
fileGradleApp.close()

# SDK Version and MultiDex
fileGradleApp = open("android/app/build.gradle", "r")
gradleApp = fileGradleApp.read()
minSDKIndex = gradleApp.find("minSdkVersion") + len("minSdkVersion")
gradleApp = gradleApp[:minSDKIndex] + " 19\n\t\tmultiDexEnabled true" + gradleApp[minSDKIndex+3:]
fileGradleApp.close()
fileGradleApp = open("android/app/build.gradle", "w")
fileGradleApp.write(gradleApp)
fileGradleApp.close()

# Pubspec.yaml
filePubspec = open("pubspec.yaml", "r")
pubspec = filePubspec.read()

cupertinoIndex = pubspec.find("cupertino_icons: ") + len("cupertino_icons: ^1.0.2")
dependecies = ["firebase_core:", "cloud_firestore:"]
pubspec = pubspec[:cupertinoIndex] + concatAll(dependecies, '\n  ') + pubspec[cupertinoIndex:]

filePubspec.close()

filePubspec = open("pubspec.yaml", "w")
filePubspec.write(pubspec)
filePubspec.close()

#print(pubspec)

# Finish
print("Pronto! (Pressione qualquer tecla para finalizar)\n")
input()