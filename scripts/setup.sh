#!/usr/bin/env bash
# This script adds the required dependencies to the project using pdm
# Usage: ./setup.sh
# SAVE_EXACT=1 ./setup.sh # To save exact versions of the dependencies

PDM_OPTIONS=""
if [[ $SAVE_EXACT -eq 1 ]]; then
    PDM_OPTIONS="${PDM_OPTIONS} --save-exact"
fi

echo -e "\033[1;32m[INFO]\033[0m Setting up the project..."
# Add the required dependencies
pdm add $PDM_OPTIONS fastapi uvicorn environs
pdm add $PDM_OPTIONS -d pre-commit

read -p "Do you want to add support for a database? [y/N] " db_support
if [[ $db_support =~ ^[Yy]$ ]]; then
    pdm add $PDM_OPTIONS -G db sqlalchemy pymysql cryptography sqlmodel
    read -p "Insert database name:" db_name
    if [ "$db_name" == "y" ]; then
        db_name="db_name"
    fi
    read -p "Insert database external port:" db_external_port
    if [ "$db_external_port" == "y" ]; then
        db_external_port="3306"
    fi

    # .env
    echo "# >>> External ports" >>.env
    echo "DB_PORT=$db_external_port" >>.env
    echo "# <<< External ports" >>.env
    echo MYSQL_ROOT_USER=root >>.env
    echo MYSQL_ROOT_PASSWORD=root >>.env
    echo MYSQL_DATABASE=$db_name >>.env
    echo 'DATABASE_URL=mysql+pymysql://${MYSQL_ROOT_USER}:${MYSQL_ROOT_PASSWORD}@db:3306/${MYSQL_DATABASE}' >>.env

    # .env.template
    echo "# >>> External ports" >>.env.template
    echo "DB_PORT=" >>.env.template
    echo "# <<< External ports" >>.env.template
    echo MYSQL_ROOT_USER=root >>.env.template
    echo MYSQL_ROOT_PASSWORD=root >>.env.template
    echo MYSQL_DATABASE= >>.env.template
    echo 'DATABASE_URL=mysql+pymysql://${MYSQL_ROOT_USER}:${MYSQL_ROOT_PASSWORD}@db:3306/${MYSQL_DATABASE}' >>.env.template
else
    echo -e "\033[1;33m[WARNING]\033[0m Skipping database support..."
fi

read -p "Do you want to add support for testing? [y/N] " test_support
if [[ $test_support =~ ^[Yy]$ ]]; then
    pdm add $PDM_OPTIONS -G test pytest pytest-asyncio coverage
else
    echo -e "\033[1;33m[WARNING]\033[0m Skipping testing support..."
fi

read -p "Do you want to add support for linting? [y/N] " lint_support
if [[ $lint_support =~ ^[Yy]$ ]]; then
    pdm add $PDM_OPTIONS -G lint ruff
else
    echo -e "\033[1;33m[WARNING]\033[0m Skipping linting support..."
fi

read -p "Do you want to add support for jupyter notebooks? [y/N] " notebook_support
if [[ $notebook_support =~ ^[Yy]$ ]]; then
    pdm add $PDM_OPTIONS -G notebook jupyter
else
    echo -e "\033[1;33m[WARNING]\033[0m Skipping jupyter notebook support..."
fi
