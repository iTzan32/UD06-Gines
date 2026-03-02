# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LigaPartido(models.Model):
    _name = 'liga.partido'
    _description = 'Un partido de la liga'

    equipo_casa = fields.Many2one('liga.equipo', string='Equipo local')
    goles_casa = fields.Integer()
    equipo_fuera = fields.Many2one('liga.equipo', string='Equipo visitante')
    goles_fuera = fields.Integer()

    @api.constrains('equipo_casa', 'equipo_fuera')
    def _check_equipos(self):
        for record in self:
            if not record.equipo_casa or not record.equipo_fuera:
                raise ValidationError('Debe seleccionar ambos equipos.')
            if record.equipo_casa == record.equipo_fuera:
                raise ValidationError('Los equipos deben ser diferentes.')

    def actualizoRegistrosEquipo(self):
        for equipo in self.env['liga.equipo'].search([]):
            equipo.victorias = equipo.empates = equipo.derrotas = 0
            equipo.goles_a_favor = equipo.goles_en_contra = 0
            equipo.puntos = 0

            for partido in self.env['liga.partido'].search([]):
                if partido.equipo_casa == equipo:
                    if partido.goles_casa > partido.goles_fuera:
                        equipo.victorias += 1
                        equipo.puntos += 4 if (partido.goles_casa - partido.goles_fuera) >= 4 else 3
                    elif partido.goles_casa < partido.goles_fuera:
                        equipo.derrotas += 1
                        equipo.puntos -= 1 if (partido.goles_fuera - partido.goles_casa) >= 4 else 0
                    else:
                        equipo.empates += 1
                        equipo.puntos += 1
                    equipo.goles_a_favor += partido.goles_casa
                    equipo.goles_en_contra += partido.goles_fuera

                if partido.equipo_fuera == equipo:
                    if partido.goles_fuera > partido.goles_casa:
                        equipo.victorias += 1
                        equipo.puntos += 4 if (partido.goles_fuera - partido.goles_casa) >= 4 else 3
                    elif partido.goles_fuera < partido.goles_casa:
                        equipo.derrotas += 1
                        equipo.puntos -= 1 if (partido.goles_casa - partido.goles_fuera) >= 4 else 0
                    else:
                        equipo.empates += 1
                        equipo.puntos += 1
                    equipo.goles_a_favor += partido.goles_fuera
                    equipo.goles_en_contra += partido.goles_casa

    # FUNCIONES PARA LOS BOTONES DE LA ACTIVIDAD 1
    def sumar_dos_goles_casa(self):
        for record in self.env['liga.partido'].search([]):
            record.goles_casa += 2
        self.actualizoRegistrosEquipo()

    def sumar_dos_goles_visitante(self):
        for record in self.env['liga.partido'].search([]):
            record.goles_fuera += 2
        self.actualizoRegistrosEquipo()

    @api.model
    def create(self, values):
        record = super().create(values)
        self.actualizoRegistrosEquipo()
        return record

    def write(self, values):
        res = super().write(values)
        self.actualizoRegistrosEquipo()
        return res

    def unlink(self):
        res = super().unlink()
        self.actualizoRegistrosEquipo()
        return res