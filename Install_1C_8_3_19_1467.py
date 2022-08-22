# -*- coding: utf-8 -*-

# ###############################
# Скрипт установки 1С:Предприятие
# ###############################

import urllib2
import os
import sys
import subprocess
import socket
import ctypes
import shutil

#
# Функция проверки наличия прав администратора
#
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

#
# Функция проверки доступности URL
#
def url_ok( url, timeout=5 ):
    try:
        return urllib2.urlopen(url,timeout=timeout).getcode() == 200
    except urllib2.URLError as e:
        return False
    except socket.timeout as e:
        return False

# Функция скачивания файла
# Вход: Откуда скачиваем файл (myurl), куда скачиваем файл (mypath)
# Выход: true  - успешное скачивание
# 		 false - скачивание не удалось
def my_downloadfile(myurl,mypath):
	if not url_ok(myurl, 5):
		print 'Файл НЕдоступен:', myurl
		return False
	print 'Файл доступен:', myurl
	try:
		mycontent = urllib2.urlopen(myurl)
		output = open(mypath,'wb')
		output.write(mycontent.read())
		output.close()
	except urllib2.HTTPError, error:
		print 'Ошибка: ', error.read()
		print 'Файл не скачан', myurl
		return False
	except:
		print 'Что-то пошло не так при скачивании файла.', myurl
		return False
	else:
		print 'Файл скачан.', myurl
		return True

if is_admin():
    print 'Прав для установки программ достаточно...'
else:
    print 'Недостаточно прав для запуска скрипта!!!'
    sys.exit('Error')

# Базовая ссылка для скачивания
my_baseurl='http://repo.mihanik.net/1C/8_3_19_1467'

# Количество частей архива для скачивания
my_count=32

print sys.version

# Скачиваем все части архива с установщиком
for i in range(1, my_count+1):
	if i < 10:
		my_url = my_baseurl + '/distr1c.zip.00' + str(i)
		my_filename = 'C:/Windows/Temp/distr1c.zip.00' + str(i)
	else:
		my_url = my_baseurl + '/distr1c.zip.0' + str(i)
		my_filename = 'C:/Windows/Temp/distr1c.zip.0' + str(i)
	
	my_err = 0
	while not my_downloadfile(my_url,my_filename):
		my_err = my_err + 1
		print 'Ошибка скачивания файла ', my_url
		if my_err > 4:
			print 'Произошло 5 ошибок скачивания.'
			print 'Установка программы прервана!'
			sys.exit('Error')

print 'Успешно скачаны все части архива!!!'

os.chdir('C:/Windows/Temp')

# Проверим наличие архиватора на компьютере
# Если архиватора нет, установим его.
if os.path.exists('C:/Program Files/7-Zip/7z.exe'):
    print 'Архиватор найден!'
else:
    print 'Архиватор НЕ найден! Устанавливаем 7Zip.'
    if not my_downloadfile('http://repo.mihanik.net/7-Zip/7z1900.exe','C:/Windows/Temp/7z1900.exe'):
        print 'Скачать архиватор не удалось.'
        sys.exit('Error!')

    if not my_downloadfile('http://repo.mihanik.net/7-Zip/7z1900-x64.exe','C:/Windows/Temp/7z1900-x64.exe'):
        print 'Скачать архиватор не удалось.'
        sys.exit('Error!')

    if os.path.exists('C:/Program Files (x86)'):
        errorCode = os.system('7z1900-x64.exe /S')
    else:
        errorCode = os.system('7z1900.exe /S')

	if errorCode == 0:
		print 'Архиватор 7Zip установлен успешно.'
	else:
		print 'При установке архиватора 7Zip произошли ошибки!'
		sys.exit('Error!!!')

# Создаём каталог C:/Windows/Temp/Mihanikus/Windows
os.chdir('C:/Windows/Temp')

try:
    shutil.rmtree('C:/Windows/Temp/Mihanikus/Windows', ignore_errors=True)
except:
    print 'Не удалось очистить папку С:/Windows/Temp/Mihanikus/Windows'
    sys.exit('Error')

try:
    if os.path.exists('C:/Windows/Temp/Mihanikus/Windows'):
        print 'Директория уже существует: C:/Windows/Temp/Mihanikus/Windows'
        print 'Останавливаем дальнейшее выполнение скрипта!'
        sys.exit('Error')
    else:
        os.makedirs('C:/Windows/Temp/Mihanikus/Windows')
except:
	print 'Что-то пошло не так при создании каталога: C:/Windows/Temp/Mihanikus/Windows'
	sys.exit('Error!')
else:
	print 'Успешно создана директория: C:/Windows/Temp/Mihanikus/Windows'

# Разархивируем дистрибутив
errorCode = os.system(r'"C:/Program Files/7-Zip/7z.exe" x C:\Windows\Temp\distr1c.zip.001 -oC:\Windows\Temp\Mihanikus\Windows -y -r')

if errorCode == 0:
	print 'Дистрибутив распакован'
else:
	print 'При распаковке возникла ошибка!!!'
	sys.exit('Error!!!')

# Переименовываем файл
if os.path.exists('C:/Windows/Temp/Mihanikus/Windows/1CEnterprise8.msi'):
    os.remove('C:/Windows/Temp/Mihanikus/Windows/1CEnterprise8.msi')

# Меняем рабочий каталог
os.chdir('C:/Windows/Temp/Mihanikus/Windows')

os.rename('C:/Windows/Temp/Mihanikus/Windows/1CEnterprise 8.msi','C:/Windows/Temp/Mihanikus/Windows/1CEnterprise8.msi')

# Устанавливаем 1С
errorCode = os.system(r'start /wait 1CEnterprise8.msi /quiet TRANSFORMS=adminstallrelogon.mst;1049.mst DESIGNERALLCLIENTS=1 THICKCLIENT=1 THINCLIENTFILE=1 THINCLIENT=1 WEBSERVEREXT=0 SERVER=0 CONFREPOSSERVER=0 CONVERTER77=0 SERVERCLIENT=0 LANGUAGES=RU')

if errorCode == 0:
	print '1С:Предприятие установлено успешно!'
elif errorCode == 1641:
	print 'The requested operation completed successfully. The system will be restarted so the changes can take effect.'
elif errorCode == 3010:
	print 'The requested operation is successful. Changes will not be effective until the system is rebooted.'
else:
	print 'При установке 1С:Предприятия возникла ошибка: ', errorCode, " !"
	sys.exit('Error!!!')

