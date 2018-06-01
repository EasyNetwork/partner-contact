from odoo import http
from odoo.http import request
import json


class BaseLocationController(http.Controller):

    @http.route('/location/country', auth="none")
    def get_countries(self, s_action=None, **kw):
        domain = []
        countries = request.env['res.country'].sudo().search(domain)
        res = {'countries': []}
        for country in countries:
            res['countries'].append(
                {
                    'name': country.name,
                    'code': country.code
                }
            )
        return json.dumps(res)

    @http.route('/api/restful', type='json', auth='public', csrf=False)
    def restful(self, **post):
        filecontent = {}
        if post.get('login') and post.get('password'):
           if not post.get('database'):
              from odoo.service.db import list_dbs
              post['database'] = list_dbs()[0]
           login = request.session.authenticate(post['database'], post['login'], post['password'])
           if not login:
              filecontent['status'] = 'denied'
              return request.make_response(json(filecontent), [('Access-Control-Allow-Origin', '*')])
           filecontent = request.env['res.users'].search([]).read()
        if not filecontent:
           filecontent = {'status': 'error'}
        return request.make_response(json(filecontent), [('Access-Control-Allow-Origin', '*')])