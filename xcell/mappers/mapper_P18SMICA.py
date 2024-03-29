from .mapper_Planck_base import MapperPlanckBase
from .utils import rotate_map
import healpy as hp
import numpy as np


class MapperP18SMICA(MapperPlanckBase):
    """
    path = `".../Datasets/Planck_SMICA"`
    **Config**

        - file_map: `path+"COM_CMB_IQU-smica-nosz_2048_R3.00_full.fits"`
        - file_hm1: `path+"COM_CMB_IQU-smica-nosz_2048_R3.00_hm1.fits"`
        - file_hm2: `path+"COM_CMB_IQU-smica-nosz_2048_R3.00_hm2.fits"`
        - file_gp_mask: \
        `".../Datasets/Planck_masks/HFI_Mask_GalPlane-apo2_2048_R2.00.fits"`
        - file_ps_mask: \
        `".../Datasets/Planck_masks/HFI_Mask_PointSrc_2048_R2.00.fits"`

        - beam_info:

            - type: `'Gaussian'`
            - FWHM_arcmin: `5.0`

        - gp_mask_mode: `'0.6'`
        - ps_mask_mode: `['F100', 'F143', 'F217', 'F353']`
        - mask_name: `mask_P18SMICA`
        - path_rerun: `'.../Datasets/Planck_SMICA/xcell_runs'`
    """
    map_name = "P18SMICA"

    def __init__(self, config):
        self._get_Planck_defaults(config)
        self.beam_info = config.get('beam_info',
                                    [{'type': 'Gaussian',
                                      'FWHM_arcmin': 5.0}])
        self.gp_mask_mode = config.get('gp_mask_mode', '0.6')
        self.gp_mask_modes = {'0.2': 0,
                              '0.4': 1,
                              '0.6': 2,
                              '0.7': 3,
                              '0.8': 4,
                              '0.9': 5,
                              '0.97': 6,
                              '0.99': 7}
        self.ps_mask_modes = {'F100': 0,
                              'F143': 1,
                              'F217': 2,
                              'F353': 3}
        self.ps_mask_mode = config.get('ps_mask_mode',
                                       ['F100', 'F143', 'F217', 'F353'])

    def _generate_hm_maps(self):
        hm1_map = hp.read_map(self.file_hm1)
        ps_mask = self._get_ps_mask()
        hm1_map *= ps_mask
        hm1_map = rotate_map(hm1_map, self.rot)
        hm1_map = hp.ud_grade(hm1_map, nside_out=self.nside)

        hm2_map = hp.read_map(self.file_hm2)
        ps_mask = self._get_ps_mask()
        hm2_map *= ps_mask
        hm2_map = rotate_map(hm2_map, self.rot)
        hm2_map = hp.ud_grade(hm2_map, nside_out=self.nside)

        return np.array([hm1_map, hm2_map])

    def get_dtype(self):
        """
        Returns the type of the mapper. \

        Args:
            None
        Returns:
            mapper_type (String)
        """
        return 'cmb_temperature'
