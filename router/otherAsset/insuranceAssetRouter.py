# -*- coding: UTF-8 -*-

from datetime import datetime
from flask import jsonify, request

from api.response_format import ResponseFormat
from app.dao.model.otherAsset.insurance_detail_model import InsuranceDetail
from app.dao.model.otherAsset.insurance_journal_model import InsuranceJournal

date_format = '%Y-%m-%dT%H:%M:%S.%fZ'


def init_insurance_asset_api(app):
    @app.route('/other-asset/insurance/<int:asset_id>', methods=['GET'])
    def getInsuranceAssets(asset_id):
        output = []

        try:
            insurance_assets = InsuranceJournal.query4Summary(
                InsuranceJournal, asset_id)
            for insurance_asset in insurance_assets:
                output.append(InsuranceJournal.output4View(
                    InsuranceJournal, insurance_asset))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/other-asset/insurance', methods=['POST'])
    def addInsuranceAsset():
        global date_format

        try:
            # force=True 忽略mimetype，只接字串
            inputData = request.get_json(force=True)

            insurance_asset = InsuranceJournal(asset_id=inputData['asset_id'], insurance_name=inputData['insurance_name'],
                                               start_date=datetime.strptime(
                                                   inputData['start_date'], date_format),
                                               expected_end_date=datetime.strptime(
                                                   inputData['expected_end_date'], date_format),
                                               pay_type=inputData['pay_type'], pay_day=inputData['pay_day'],
                                               in_account_id=inputData['in_account_id'], in_account_name=inputData['in_account_name'],
                                               out_account_id=inputData['out_account_id'], out_account_name=inputData['out_account_name'],
                                               expected_spend=inputData['expected_spend'], has_closed=inputData['has_closed'])
            result = InsuranceJournal.add(InsuranceJournal, insurance_asset)

            if result:
                return jsonify(ResponseFormat.true_return(ResponseFormat, InsuranceJournal.output(InsuranceJournal, result)))
            else:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to add insurance data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/other-asset/insurance/<int:insurance_id>', methods=['PUT'])
    def updateInsuranceAsset(insurance_id):
        try:
            insurance_asset = InsuranceJournal.queryByKey(
                InsuranceJournal, insurance_id)
            if insurance_asset is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                inputData = request.get_json(force=True)

                insurance_asset.insurance_name = inputData['insurance_name']
                insurance_asset.pay_type = inputData['pay_type']
                insurance_asset.pay_day = inputData['pay_day']
                insurance_asset.in_account_id = inputData['in_account_id']
                insurance_asset.in_account_name = inputData['in_account_name']
                insurance_asset.out_account_id = inputData['out_account_id']
                insurance_asset.out_account_name = inputData['out_account_name']
                # insurance_asset.expected_spend = inputData['expected_spend'] if inputData['expected_spend'] else None
                if InsuranceJournal.update(InsuranceJournal):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to update insurance data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/other-asset/insurance/<int:insurance_id>', methods=['DELETE'])
    def deleteInsuranceAsset(insurance_id):
        try:
            insurance_asset = InsuranceJournal.queryByKey(
                InsuranceJournal, insurance_id)
            if insurance_asset is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                if InsuranceJournal.delete(InsuranceJournal, insurance_id):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to delete insurance data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/other-asset/insurance/detail/<int:insurance_id>', methods=['GET'])
    def getInsuranceDetails(insurance_id):
        output = []

        try:
            insurance_details = InsuranceDetail.queryByInsuranceId(
                InsuranceDetail, insurance_id)
            for insurance_detail in insurance_details:
                output.append(InsuranceDetail.output(
                    InsuranceDetail, insurance_detail))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
        else:
            return jsonify(ResponseFormat.true_return(ResponseFormat, output))

    @app.route('/other-asset/insurance/detail', methods=['POST'])
    def addInsuranceDetail():
        global date_format

        try:
            # force=True 忽略mimetype，只接字串
            inputData = request.get_json(force=True)

            insurance_detail = InsuranceDetail(insurance_id=inputData['insurance_id'], insurance_excute_type=inputData['insurance_excute_type'],
                                               excute_price=inputData['excute_price'], excute_date=datetime.strptime(
                                                   inputData['excute_date'], date_format),
                                               memo=inputData['memo'])
            result = InsuranceDetail.add(InsuranceDetail, insurance_detail)

            if result:
                return jsonify(ResponseFormat.true_return(ResponseFormat, InsuranceDetail.output(InsuranceDetail, result)))
            else:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to add insurance detail data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/other-asset/insurance/detail/<int:distinct_number>', methods=['PUT'])
    def updateInsuranceDetail(distinct_number):
        global date_format

        try:
            insurance_detail = InsuranceDetail.queryByKey(
                InsuranceDetail, distinct_number)
            if insurance_detail is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                inputData = request.get_json(force=True)

                insurance_detail.insurance_excute_type = inputData['insurance_excute_type']
                insurance_detail.excute_price = inputData['excute_price']
                insurance_detail.excute_date = datetime.strptime(
                    inputData['excute_date'], date_format)
                insurance_detail.memo = inputData['memo']

                if InsuranceDetail.update(InsuranceDetail):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to update insurance detail data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))

    @app.route('/other-asset/insurance/detail/<int:distinct_number>', methods=['DELETE'])
    def deleteInsuranceDetail(distinct_number):
        try:
            insurance_detail = InsuranceDetail.queryByKey(
                InsuranceDetail, distinct_number)
            if insurance_detail is None:
                return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'data not found'))
            else:
                if InsuranceDetail.delete(InsuranceDetail, distinct_number):
                    return jsonify(ResponseFormat.true_return(ResponseFormat, None))
                else:
                    return jsonify(ResponseFormat.false_return(ResponseFormat, None, 'fail to delete insurance detail data'))
        except Exception as error:
            return jsonify(ResponseFormat.false_return(ResponseFormat, error))
