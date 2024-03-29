from .utils import rotate_map
from .mapper_Planck_base import MapperPlanckBase
import healpy as hp
import numpy as np


class MapperP15tSZ(MapperPlanckBase):
    """
    path = `".../Datasets/Planck_tSZ"`

    **Config**

        - file_map: `path+"COM_CompMap_YSZ_R2.02/milca_ymaps.fits"`
        - file_gp_mask: \
        `path+"COM_CompMap_YSZ_R2.02/COM_CompMap_Compton-SZMap-masks_2048_R2.01.fits"`
        - file_ps_mask: \
        `".../Datasets/Planck_tSZ/COM_CompMap_YSZ_R2.02/COM_CompMap_Compton-SZMap-masks_2048_R2.01.fits"`
        - gp_mask_mode: `'0.6'`
        - ps_mask_mode: `['default']`
        - beam_info:

            - type: `'Gaussian'`
            - FWHM_arcmin: `10.0`

        - mask_name: `mask_P15tSZ`
        - path_rerun: `path+"COM_CompMap_YSZ_R2.02/xcell_runs"`
    """
    map_name = "P15tSZ"

    def __init__(self, config):
        self._get_Planck_defaults(config)
        self.file_hm1 = config.get('file_hm1', self.file_map)
        self.file_hm2 = config.get('file_hm2', self.file_map)
        self.beam_info = config.get('beam_info',
                                    [{'type': 'Gaussian',
                                      'FWHM_arcmin': 10.0}])
        self.gp_mask_mode = config.get('gp_mask_mode', '0.5')
        self.gp_mask_modes = {'0.4': 0,
                              '0.5': 1,
                              '0.6': 2,
                              '0.7': 3}
        self.ps_mask_mode = config.get('ps_mask_mode', ['default'])
        self.ps_mask_modes = {'test': 0,
                              'default': 4}

    def _generate_hm_maps(self):
        hm1_map = hp.read_map(self.file_hm1, 1)
        ps_mask = self._get_ps_mask()
        hm1_map *= ps_mask
        hm1_map = rotate_map(hm1_map, self.rot)
        hm1_map = hp.ud_grade(hm1_map, nside_out=self.nside)

        hm2_map = hp.read_map(self.file_hm2, 2)
        ps_mask = self._get_ps_mask()
        hm2_map *= ps_mask
        hm2_map = rotate_map(hm2_map, self.rot)
        hm2_map = hp.ud_grade(hm2_map, nside_out=self.nside)

        return np.array([hm1_map, hm2_map])

    def get_dtype(self):
        return 'cmb_tSZ'
