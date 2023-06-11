import os
import secrets
import smtplib
import sqlite3
import ssl
from datetime import datetime
from email.message import EmailMessage
from os import mkdir
from os.path import exists
from random import randint

from flask import (
    Blueprint, Flask, flash, redirect, render_template, request, send_from_directory, session
)
from passlib.hash import sha256_crypt

from forms import (
    changePasswordForm, changeUserNameForm, commentForm, createPostForm, loginForm,
    passwordResetForm, signUpForm
)


def currentDate():
    return datetime.now().strftime("%d.%m.%y")


def currentTime(seconds=False):
    match seconds:
        case False:
            return datetime.now().strftime("%H:%M")
        case True:
            return datetime.now().strftime("%H:%M:%S")


def message(color, message):
    print(
        f"\n\033[94m[{currentDate()}\033[0m"
        f"\033[95m {currentTime(True)}]\033[0m"
        f"\033[9{color}m {message}\033[0m\n"
    )
    logFile = open("log.log", "a")
    logFile.write(f"[{currentDate()}" f"|{currentTime(True)}]" f" {message}\n")
    logFile.close()


def addPoints(points, user):
    connection = sqlite3.connect("db/users.db")
    cursor = connection.cursor()
    cursor.execute(
        f'update users set points = points+{points} where userName = "{user}"'
    )
    connection.commit()
    message("2", f'{points} POINTS ADDED TO "{user}"')


def getProfilePicture(userName):
    connection = sqlite3.connect("db/users.db")
    cursor = connection.cursor()
    cursor.execute(
        f'select profilePicture from users where lower(userName) = "{userName.lower()}"'
    )
    return cursor.fetchone()[0]
