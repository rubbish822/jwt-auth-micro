# coding: utf-8


class JwtDecodeError(Exception):
    def __str__(self):
        return f'Jwt decode failed!'


class JwtExpireError(Exception):
    def __str__(self):
        return f'Jwt token expired!'


class JwtNotRightError(Exception):
    def __str__(self):
        return f'Jwt token not right!'


class TokenHeaderError(Exception):
    def __str__(self):
        return f'The header not have token!'



