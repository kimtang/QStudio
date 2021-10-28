@rem
@rem Copyright 2015 the original author or authors.
@rem
@rem Licensed under the Apache License, Version 2.0 (the "License");
@rem you may not use this file except in compliance with the License.
@rem You may obtain a copy of the License at
@rem
@rem      https://www.apache.org/licenses/LICENSE-2.0
@rem
@rem Unless required by applicable law or agreed to in writing, software
@rem distributed under the License is distributed on an "AS IS" BASIS,
@rem WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
@rem See the License for the specific language governing permissions and
@rem limitations under the License.
@rem

@if "%DEBUG%" == "" @echo off
@rem ##########################################################################
@rem
@rem  kdb-studio startup script for Windows
@rem
@rem ##########################################################################

@rem Set local scope for the variables with windows NT shell
if "%OS%"=="Windows_NT" setlocal

set DIRNAME=%~dp0
if "%DIRNAME%" == "" set DIRNAME=.
set APP_BASE_NAME=%~n0
set APP_HOME=%DIRNAME%..

@rem Resolve any "." and ".." in APP_HOME to make it shorter.
for %%i in ("%APP_HOME%") do set APP_HOME=%%~fi

@rem Add default JVM options here. You can also use JAVA_OPTS and KDB_STUDIO_OPTS to pass JVM options to this script.
set DEFAULT_JVM_OPTS=

@rem Find java.exe
if defined JAVA_HOME goto findJavaFromJavaHome

set JAVA_EXE=java.exe
%JAVA_EXE% -version >NUL 2>&1
if "%ERRORLEVEL%" == "0" goto execute

echo.
echo ERROR: JAVA_HOME is not set and no 'java' command could be found in your PATH.
echo.
echo Please set the JAVA_HOME variable in your environment to match the
echo location of your Java installation.

goto fail

:findJavaFromJavaHome
set JAVA_HOME=%JAVA_HOME:"=%
set JAVA_EXE=%JAVA_HOME%/bin/java.exe

if exist "%JAVA_EXE%" goto execute

echo.
echo ERROR: JAVA_HOME is set to an invalid directory: %JAVA_HOME%
echo.
echo Please set the JAVA_HOME variable in your environment to match the
echo location of your Java installation.

goto fail

:execute
@rem Setup the command line

set CLASSPATH=%APP_HOME%\lib\kdb-studio.jar;%APP_HOME%\lib\org-openide-awt-RELEASE113.jar;%APP_HOME%\lib\jfreechart-1.0.14.jar;%APP_HOME%\lib\poi-ooxml-4.1.2.jar;%APP_HOME%\lib\poi-4.1.2.jar;%APP_HOME%\lib\jackson-databind-2.11.2.jar;%APP_HOME%\lib\org-netbeans-api-annotations-common-RELEASE113.jar;%APP_HOME%\lib\org-openide-filesystems-RELEASE113.jar;%APP_HOME%\lib\org-openide-util-ui-RELEASE113.jar;%APP_HOME%\lib\org-openide-util-RELEASE113.jar;%APP_HOME%\lib\org-openide-util-lookup-RELEASE113.jar;%APP_HOME%\lib\jcommon-1.0.17.jar;%APP_HOME%\lib\xml-apis-1.3.04.jar;%APP_HOME%\lib\itext-2.1.5.jar;%APP_HOME%\lib\commons-codec-1.13.jar;%APP_HOME%\lib\commons-collections4-4.4.jar;%APP_HOME%\lib\commons-math3-3.6.1.jar;%APP_HOME%\lib\SparseBitSet-1.2.jar;%APP_HOME%\lib\poi-ooxml-schemas-4.1.2.jar;%APP_HOME%\lib\commons-compress-1.19.jar;%APP_HOME%\lib\curvesapi-1.06.jar;%APP_HOME%\lib\jackson-annotations-2.11.2.jar;%APP_HOME%\lib\jackson-core-2.11.2.jar;%APP_HOME%\lib\bcmail-jdk14-138.jar;%APP_HOME%\lib\bcprov-jdk14-138.jar;%APP_HOME%\lib\xmlbeans-3.1.0.jar


@rem Execute kdb-studio
"%JAVA_EXE%" %DEFAULT_JVM_OPTS% %JAVA_OPTS% %KDB_STUDIO_OPTS%  -classpath "%CLASSPATH%" studio.core.Studio %*

:end
@rem End local scope for the variables with windows NT shell
if "%ERRORLEVEL%"=="0" goto mainEnd

:fail
rem Set variable KDB_STUDIO_EXIT_CONSOLE if you need the _script_ return code instead of
rem the _cmd.exe /c_ return code!
if  not "" == "%KDB_STUDIO_EXIT_CONSOLE%" exit 1
exit /b 1

:mainEnd
if "%OS%"=="Windows_NT" endlocal

:omega
