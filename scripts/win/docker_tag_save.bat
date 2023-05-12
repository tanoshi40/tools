@ECHO OFF

:: NOTE set service_name

:: This script will get the git branch and search for the prefix-ticketnumber
:: Example: feature/AUGVIS-12345-do-some-stuff
:: This would extract to "AUGVIS-12345"
:: Expected branch format: something/PREFIX-TICKETNUM-something

:: After extracting the ticket number tag the tag the build docker image and save it to disk

:: -- CONFIG --
SET service_name=TODO

SET registry=via-docker-registry-snapshot.devops.in.idemia.com
SET registry_path=idemia
SET image_version=dev-SNAPSHOT

:: -- SCRIPT --

SET base_docker=%registry%/%registry_path%/%service_name%:%image_version%
SET out=%service_name%.tar

SET branch_command='git rev-parse --abbrev-ref HEAD'

FOR /f %%i IN (%branch_command%) DO SET branch=%%i
ECHO branch: "%branch%"

FOR /f "tokens=2 delims=/-" %%i IN (%branch_command%) DO SET prefix=%%i
FOR /f "tokens=2 delims=/%prefix%-" %%i IN (%branch_command%) DO SET branch_num=%%i

SET branch_tag=%prefix%-%branch_num%
SET docker_image=%base_docker%-%branch_tag%

ECHO branch tag: "%branch_tag%"
ECHO image tag: "%docker_image%"

ECHO tagging image %docker_image% to %service_name%
docker tag %docker_image% %service_name%

ECHO saving docker image to "%out%"
docker save -o %out% %service_name%
