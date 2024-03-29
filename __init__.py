# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ProfilUlice
                                 A QGIS plugin
 Vytvoří profil ulice zvolené linie
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2022-03-30
        copyright            : (C) 2022 by Jakub Vynikal
        email                : jakub.vynikal@fsv.cvut.cz
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load ProfilUlice class from file ProfilUlice.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .profil_ulice import ProfilUlice
    return ProfilUlice(iface)
