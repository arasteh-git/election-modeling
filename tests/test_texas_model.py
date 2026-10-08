"""The src/ refactor must reproduce the notebook results exactly.

Expected values are the saved outputs of notebooks/data-pulls.ipynb at commit
ccb41c0 (and STATUS.md / docs/methodology.md). Nothing here re-decides the model.
"""
import unittest

from src.model.run_texas import forecast


class TexasForecastRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.f = forecast()

    def test_texas_average_and_n_eff(self):
        self.assertEqual(self.f['n_polls'], 14)
        self.assertEqual(round(self.f['avg'], 3), 3.952)
        self.assertEqual(round(self.f['n_eff'], 3), 6.705)
        # Full-precision values printed by the notebook.
        self.assertAlmostEqual(self.f['avg'], 3.951961744801757, places=12)
        self.assertAlmostEqual(self.f['n_eff'], 6.705115664083077, places=12)

    def test_sigma_and_probability(self):
        self.assertEqual(round(self.f['sigma'], 3), 7.030)
        self.assertAlmostEqual(self.f['sigma'], 7.029683, places=6)
        self.assertEqual(round(self.f['p_dem'], 3), 0.713)
        self.assertAlmostEqual(self.f['p_dem'], 0.7130040229861502, places=12)

    def test_calibration_by_horizon(self):
        table = self.f['by_horizon']
        self.assertEqual(list(table.index), [7, 14, 28, 42])
        self.assertEqual(list(table['races']), [50, 50, 50, 47])
        self.assertEqual(list(table['rmse'].round(2)), [6.50, 6.80, 7.03, 6.45])
        self.assertEqual(list(table['mean_error'].round(2)), [-2.84, -3.16, -3.87, -3.10])
        notebook_rmse = [6.495299, 6.803297, 7.029683, 6.448441]
        for got, want in zip(table['rmse'], notebook_rmse):
            self.assertAlmostEqual(got, want, places=6)

    def test_dropped_contest_horizons(self):
        dropped = set(map(tuple, self.f['dropped'].to_numpy()))
        expected = {(f'{y}-WY-ordinary-general', h) for y in (2018, 2020) for h in (7, 14, 28, 42)}
        expected |= {(f'2020-{s}-ordinary-general', 42) for s in ('DE', 'OR', 'WV')}
        self.assertEqual(dropped, expected)
        self.assertEqual(len(self.f['errors']), 197)

    def test_mean_error_by_cycle(self):
        me = self.f['by_cycle']['mean_error'].round(6)
        self.assertEqual(me.loc[('2018', 7)], -0.117469)
        self.assertEqual(me.loc[('2018', 42)], -1.829807)
        self.assertEqual(me.loc[('2020', 28)], -6.541015)
        self.assertEqual(me.loc[('2020', 42)], -4.801294)


if __name__ == '__main__':
    unittest.main()
