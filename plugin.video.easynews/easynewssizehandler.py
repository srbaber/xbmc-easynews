import easynewssearchhandler


#
# handler responsible for performing the size search for easynews
#
class EasynewsSizeHandler(easynewssearchhandler.EasynewsSearchHandler):
    name = 'EasynewsSizeHandler'
    searchBySize = 'SearchAndOrderBySize'

    def __init__(self):
        pass

    def build_params(self, action):
        params = super().build_params(action)
        params['s1'] = easynewssearchhandler.SORT_BY_SIZE
        params['s3'] = easynewssearchhandler.SORT_BY_DATE
        return params
