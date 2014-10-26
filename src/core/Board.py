from core.Building import Building


class Board():

	_shipPosition = 2
	_shipIsRed = False

	_buildings = {}

	def __init__(self):
		self._buildings = {
			'church': Building('church'),
			'draw_well': Building('draw_well'),
			'fair': Building('fair'),
			'draw_well': Building('draw_well'),
			'draw_well': Building('draw_well'),
			'draw_well': Building('draw_well'),
			'draw_well': Building('draw_well'),
			'draw_well': Building('draw_well'),
			'draw_well': Building('draw_well'),
		}
