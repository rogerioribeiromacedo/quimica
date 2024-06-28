# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 23:15:52 2024

@author: rogerio
"""


class Titulacao:
    def __init__(self, acido, c_acido, v_acido, base, c_base, ka, pka):
        """Init class."""
        self.acido = acido
        self.c_acido = c_acido
        self.v_acido = v_acido
        self.base = base
        self.c_base = c_base
        self.ka = ka
        self.pka = pka

    def getAcido(self):
        return self.acido

    def getCAcido(self):
        return self.c_acido

    def getVAcido(self):
        return self.v_acido

    def getBase(self):
        return self.base

    def getCBase(self):
        return self.c_base

    def getKa(self):
        return self.ka

    def getPka(self):
        return self.pka
