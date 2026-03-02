from odoo import models, fields, api

class LigaPartidoWizard(models.TransientModel):
    _name = 'liga.partido.wizard'
    _description = 'Wizard para crear partidos'

    equipo_casa = fields.Many2one('liga.equipo', string='Equipo Local', required=True)
    goles_casa = fields.Integer('Goles Local')
    equipo_fuera = fields.Many2one('liga.equipo', string='Equipo Visitante', required=True)
    goles_fuera = fields.Integer('Goles Visitante')

    def crear_partido(self):
        self.env['liga.partido'].create({
            'equipo_casa': self.equipo_casa.id,
            'goles_casa': self.goles_casa,
            'equipo_fuera': self.equipo_fuera.id,
            'goles_fuera': self.goles_fuera,
        })