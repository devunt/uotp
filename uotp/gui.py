import wx
import yaml
from pathlib import Path

from .packet import IssueRequest, TimeRequest
from . import UOTP


class MainWindow(wx.Frame):
    CONFIG_PATH = '~/.config/uotp/config.yml'
    REFRESH_INTERVAL = 30

    def __init__(self):
        super().__init__(
            None,
            title='μOTP+',
            size=(320, 240),
            style=wx.CAPTION | wx.MINIMIZE_BOX | wx.CLOSE_BOX,
        )

        path = Path(self.CONFIG_PATH).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            self.config_fp = open(str(path), 'r+', encoding='utf-8')
            self.config = yaml.load(self.config_fp)
        else:
            self.config_fp = open(str(path), 'w', encoding='utf-8')
            self.config = {
                'account': None,
                'timediff': 0,
            }
            self.save_config()

        if not self.config['account']:
            self.issue()

        wrapper = wx.Panel(self)
        sizer_wrapper = wx.BoxSizer(wx.VERTICAL)

        self.wg_gauge_time = wx.Gauge(wrapper, range=self.REFRESH_INTERVAL, style=wx.GA_HORIZONTAL | wx.GA_SMOOTH)
        sizer_wrapper.Add(self.wg_gauge_time, flag=wx.EXPAND)

        panel = wx.Panel(wrapper)
        box = wx.BoxSizer(wx.VERTICAL)

        self.wg_txt_token = wx.TextCtrl(panel, style=wx.TE_READONLY | wx.TE_CENTRE | wx.BORDER_NONE)
        self.wg_txt_token.SetFont(wx.Font(32, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        self.wg_txt_token.SetLabelText('INITIALIZING')
        box.Add(self.wg_txt_token, flag=wx.EXPAND)

        box.AddSpacer(60)

        box.Add(wx.StaticText(panel, label="S/N"), flag=wx.ALIGN_CENTRE)

        box.AddSpacer(5)

        self.wg_txt_serial = wx.TextCtrl(panel, style=wx.TE_READONLY | wx.TE_CENTRE | wx.BORDER_NONE)
        self.wg_txt_serial.SetLabelText(self.config['account']['serial_number'])
        box.Add(self.wg_txt_serial, flag=wx.ALIGN_CENTRE)

        panel.SetSizer(box)
        sizer_wrapper.Add(panel, proportion=1, flag=wx.ALL | wx.EXPAND, border=20)
        wrapper.SetSizer(sizer_wrapper)

        self.uotp = UOTP(
            self.config['account']['user_hash'].decode(),
            self.config['account']['oid'],
            self.config['account']['seed'],
            self.config['account']['serial_number']
        )
        self.uotp.sync_time()

        self.timeout = -1
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_update, self.timer)
        self.timer.Start(1000)

        self.on_update()

        self.Centre()
        self.Show()

    def issue(self):
        req = IssueRequest()
        req['mno'] = 'KTF'
        req['hw_id'] = 'GA15'
        req['hw_model'] = 'SM-N900P'
        req['version'] = (2, 0)

        resp = req()
        self.config['account'] = resp.params
        self.save_config()

    def save_config(self):
        self.config_fp.seek(0)
        yaml.dump(self.config, self.config_fp, default_flow_style=False)

    def on_update(self, event=None):
        self.timeout -= 1
        if self.timeout < 0:
            self.timeout = self.REFRESH_INTERVAL
            self.wg_txt_token.SetValue(self.uotp.generate_token())
        self.wg_gauge_time.SetValue(self.timeout)


if __name__ == '__main__':
    app = wx.App()
    MainWindow()
    app.MainLoop()
