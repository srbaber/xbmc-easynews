import easynewssearchhandler


#
# handler responsible for performing the size search for easynews
#
class EasynewsSizeHandler(easynewssearchhandler.EasynewsSearchHandler):
    name = 'EasynewsSizeHandler'
    search_by_size_operation = 'SearchAndOrderBySize'

    def build_params(self, action):
        params = super().build_params(action)
        params['s1'] = easynewssearchhandler.SORT_BY_SIZE
        params['s3'] = easynewssearchhandler.SORT_BY_DATE
        return params
