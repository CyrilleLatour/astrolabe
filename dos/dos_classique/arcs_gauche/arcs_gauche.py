def generer_arcs_gauche():
    """Génère tous les arcs du côté gauche du dos de l'astrolabe"""
    
    return {
        'arcs_interieurs': generer_arcs_interieurs(),
        'arcs_calcules': generer_arcs_calcules(),
        'segments_completion': generer_segments_completion()
    }

def generer_arcs_interieurs():
    """Génère les arcs de cercle intérieurs (rayons fixes)"""
    
    arcs = []
    rayons = [0.7125, 1.425, 2.1375, 2.85, 3.5625, 4.275, 4.9875, 5.7, 6.4125, 7.125, 7.8375]
    
    for rayon in rayons:
        arcs.append({
            'rayon': rayon,
            'stroke': 'black',
            'stroke_width': 0.05,
            'fill': 'none'
        })
    
    return arcs

def generer_arcs_calcules():
    """Génère les arcs calculés avec la méthode des sécantes"""
    
    arcs = []
    
    # Premier arc (existant)
    arcs.append({
        'path': 'M -7.8375 0 A 17.8644 17.8644 0 0 0 -8.4769 -1.116',
        'stroke': 'black',
        'stroke_width': 0.03,
        'fill': 'none',
        'commentaire': 'premier arc'
    })
    
    # Deuxième arc (existant)
    arcs.append({
        'path': 'M -7.125 0 A 17.2516 17.2516 0 0 1 -8.2587 -2.2129',
        'stroke': 'black',
        'stroke_width': 0.03,
        'fill': 'none',
        'commentaire': 'deuxième arc'
    })
    
    # Troisième arc (existant)
    arcs.append({
        'path': 'M -6.4125 0.0000 A 15.1873 15.1873 0 0 1 -7.8992 -3.2719',
        'stroke': 'black',
        'stroke_width': 0.03,
        'fill': 'none',
        'commentaire': 'troisième arc'
    })
    
    # Quatrième arc (existant)
    arcs.append({
        'path': 'M -5.7 0 A 15.0816 15.0816 0 0 1 -7.4045 -4.2750',
        'stroke': 'black',
        'stroke_width': 0.03,
        'fill': 'none',
        'commentaire': 'quatrième arc'
    })
    
    # Cinquième arc (existant)
    arcs.append({
        'path': 'M -5 0 A 13.2198 13.2198 0 0 1 -6.3484 -3.2347',
        'stroke': 'black',
        'stroke_width': 0.03,
        'fill': 'none',
        'commentaire': 'cinquième arc'
    })
    
    # Sixième arc (existant)
    arcs.append({
        'path': 'M -4.275 0 A 13.1437 13.1437 0 0 1 -5.5534 -3.2063',
        'stroke': 'black',
        'stroke_width': 0.03,
        'fill': 'none',
        'commentaire': 'sixième arc'
    })
    
    # Septième arc (calculé avec méthode des sécantes)
    arcs.append({
        'path': 'M -3.5625 0 A 10.51 10.51 0 0 1 -4.7394 -3.1668',
        'stroke': 'black',
        'stroke_width': 0.03,
        'fill': 'none',
        'commentaire': 'septième arc'
    })
    
    # Huitième arc (calculé avec méthode des sécantes)
    arcs.append({
        'path': 'M -2.85 0 A 9.23 9.23 0 0 1 -3.7023 -2.1375',
        'stroke': 'black',
        'stroke_width': 0.03,
        'fill': 'none',
        'commentaire': 'huitième arc'
    })
    
    # Neuvième arc (calculé avec méthode des sécantes)
    arcs.append({
        'path': 'M -2.1375 0 A 9.972011111 9.972011111 0 0 1 -2.8649 -2.1175',
        'stroke': 'black',
        'stroke_width': 0.03,
        'fill': 'none',
        'commentaire': 'neuvième arc'
    })
    
    # Dixième arc (calculé avec méthode des sécantes)
    arcs.append({
        'path': 'M -1.425 0 A 7.512068966 7.512068966 0 0 1 -2.0153 -2.0153',
        'stroke': 'black',
        'stroke_width': 0.03,
        'fill': 'none',
        'commentaire': 'dixième arc'
    })
    
    # Onzième arc (calculé avec méthode des sécantes)
    arcs.append({
        'path': 'M -0.7125 0 A 6.448571429 6.448571429 0 0 1 -1.0687 -1.8511',
        'stroke': 'black',
        'stroke_width': 0.03,
        'fill': 'none',
        'commentaire': 'onzième arc'
    })
    
    return arcs

def generer_segments_completion():
    """Génère tous les segments de droite qui complètent les arcs"""
    
    segments = []
    
    # Segments du cinquième arc
    segments_5 = [
        {'x1': -6.3484, 'y1': -3.2347, 'x2': -6.5933, 'y2': -4.2373},
        {'x1': -6.5933, 'y1': -4.2373, 'x2': -6.7832, 'y2': -5.2049}
    ]
    
    # Segments du sixième arc
    segments_6 = [
        {'x1': -5.5534, 'y1': -3.2063, 'x2': -5.7642, 'y2': -4.188},
        {'x1': -5.7642, 'y1': -4.188, 'x2': -5.9232, 'y2': -5.1325},
        {'x1': -5.9232, 'y1': -5.1325, 'x2': -6.0458, 'y2': -6.0458}
    ]
    
    # Segments du septième arc
    segments_7 = [
        {'x1': -4.7394, 'y1': -3.1668, 'x2': -4.9123, 'y2': -4.1219},
        {'x1': -4.9123, 'y1': -4.1219, 'x2': -5.0381, 'y2': -5.0381},
        {'x1': -5.0381, 'y1': -5.0381, 'x2': -5.1325, 'y2': -5.9232},
        {'x1': -5.1325, 'y1': -5.9232, 'x2': -5.2049, 'y2': -6.7832}
    ]
    
    # Segments du huitième arc
    segments_8 = [
        {'x1': -3.7023, 'y1': -2.1375, 'x2': -3.8994, 'y2': -3.1097},
        {'x1': -3.8994, 'y1': -3.1097, 'x2': -4.0305, 'y2': -4.0305},
        {'x1': -4.0305, 'y1': -4.0305, 'x2': -4.1219, 'y2': -4.9123},
        {'x1': -4.1219, 'y1': -4.9123, 'x2': -4.1880, 'y2': -5.7642},
        {'x1': -4.1880, 'y1': -5.7642, 'x2': -4.2373, 'y2': -6.5933},
        {'x1': -4.2373, 'y1': -6.5933, 'x2': -4.275, 'y2': -7.4045}
    ]
    
    # Segments du neuvième arc
    segments_9 = [
        {'x1': -2.8649, 'y1': -2.1175, 'x2': -3.0229, 'y2': -3.0229},
        {'x1': -3.0229, 'y1': -3.0229, 'x2': -3.1097, 'y2': -3.8994},
        {'x1': -3.1097, 'y1': -3.8994, 'x2': -3.1668, 'y2': -4.7394},
        {'x1': -3.1668, 'y1': -4.7394, 'x2': -3.2063, 'y2': -5.5534},
        {'x1': -3.2063, 'y1': -5.5534, 'x2': -3.2347, 'y2': -6.3484},
        {'x1': -3.2347, 'y1': -6.3484, 'x2': -3.2558, 'y2': -7.1292},
        {'x1': -3.2558, 'y1': -7.1292, 'x2': -3.2719, 'y2': -7.8992}
    ]
    
    # Segments du dixième arc
    segments_10 = [
        {'x1': -2.0153, 'y1': -2.0153, 'x2': -2.094, 'y2': -2.8821},
        {'x1': -2.094, 'y1': -2.8821, 'x2': -2.1375, 'y2': -3.7023},
        {'x1': -2.1375, 'y1': -3.7023, 'x2': -2.164, 'y2': -4.4936},
        {'x1': -2.164, 'y1': -4.4936, 'x2': -2.1813, 'y2': -5.2661},
        {'x1': -2.1813, 'y1': -5.2661, 'x2': -2.1932, 'y2': -6.0258},
        {'x1': -2.1932, 'y1': -6.0258, 'x2': -2.2017, 'y2': -6.7763},
        {'x1': -2.2017, 'y1': -6.7763, 'x2': -2.2081, 'y2': -7.52},
        {'x1': -2.2081, 'y1': -7.52, 'x2': -2.2129, 'y2': -8.2587}
    ]
    
    # Segments du onzième arc
    segments_11 = [
        {'x1': -1.0687, 'y1': -1.8511, 'x2': -1.0906, 'y2': -2.6331},
        {'x1': -1.0906, 'y1': -2.6331, 'x2': -1.1009, 'y2': -3.3881},
        {'x1': -1.1009, 'y1': -3.3881, 'x2': -1.1065, 'y2': -4.1293},
        {'x1': -1.1065, 'y1': -4.1293, 'x2': -1.1098, 'y2': -4.8625},
        {'x1': -1.1098, 'y1': -4.8625, 'x2': -1.112, 'y2': -5.5905},
        {'x1': -1.112, 'y1': -5.5905, 'x2': -1.1135, 'y2': -6.3151},
        {'x1': -1.1135, 'y1': -6.3151, 'x2': -1.1146, 'y2': -7.0373},
        {'x1': -1.1146, 'y1': -7.0373, 'x2': -1.1154, 'y2': -7.7577},
        {'x1': -1.1154, 'y1': -7.7577, 'x2': -1.116, 'y2': -8.4769}
    ]
    
    # Ajouter tous les segments avec leurs propriétés de style
    for segment_list in [segments_5, segments_6, segments_7, segments_8, segments_9, segments_10, segments_11]:
        for seg in segment_list:
            segments.append({
                'x1': seg['x1'], 'y1': seg['y1'],
                'x2': seg['x2'], 'y2': seg['y2'],
                'stroke': 'black',
                'stroke_width': 0.03,
                'fill': 'none'
            })
    
    return segments