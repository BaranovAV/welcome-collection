def make_decisions(input_filename):
    from lxml import etree
    from datetime import datetime

    def create_xml_2(dict_of_clients: dict):
        with open("response_task1.xml", "wb") as new_file:
            response = etree.Element("Response")
            for key, value in dict_of_clients.items():
                client_number = value["client_number"]
                sms_type = value["sms_type"]
                sms_text = value["sms_text"]
                decision_date = value["decision_date"]
                decision = etree.SubElement(response, "decision")
                client_number_element = etree.SubElement(decision, "clientNumber")
                client_number_element.text = client_number
                decision_type_element = etree.SubElement(decision, "DecisionType")
                decision_type_element.text = "SMS"
                sms_type_element = etree.SubElement(decision, "smsType")
                sms_type_element.text = sms_type
                sms_text_element = etree.SubElement(decision, "smsText")
                sms_text_element.text = sms_text
                decision_date_element = etree.SubElement(decision, "decisionDate")
                decision_date_element.text = decision_date
            new_tree = etree.ElementTree(response)
            new_tree.write(new_file, xml_declaration=True, encoding='UTF-8', pretty_print=True, standalone=True)


    def get_overdue_contracts(contracts) -> dict:
        counter = 0
        _dict = {}
        for contract in contracts:
            client_number_cnt = counter
            client_number = contract.getparent().find("clientNumber").text
            application_date = contract.getparent().find("applicationDate").text
            try:
                contract_number = contract.find("contractNumber").text
                total_overdue = contract.find("totalOverdue").text
                if int(total_overdue) > 0:
                    sms_type = "1"
                    sms_text = f"На {application_date} по контракту {contract_number} образовалась просрочка в размере {total_overdue} р"
                    _dict[str(client_number_cnt)] = {
                        "client_number": client_number,
                        "sms_type": sms_type,
                        "sms_text": sms_text,
                        "decision_date": application_date}
                else:
                    sms_type = "2"
                    next_payment = contract.find("nextPayment")
                    next_payment_date = next_payment.find("nextPaymentDate").text
                    next_payment_date_dt = datetime.strptime(next_payment_date, '%Y-%m-%d')
                    application_date_dt = datetime.strptime(application_date, '%Y-%m-%d')
                    delta = abs((next_payment_date_dt - application_date_dt).days)
                    account_balance = contract.find("accountBalance").text
                    next_payment_sum = next_payment.find("nextPaymentSum").text
                    debt = int(account_balance) - int(next_payment_sum)
                    if 5 <= delta <= 7 and debt < 0:
                        sms_text = f"Напоминаем о предстоящем платеже по контракту {contract_number} в размере {next_payment_sum} р "
                        _dict[str(client_number_cnt)] = {
                            "client_number": client_number,
                            "sms_type": sms_type,
                            "sms_text": sms_text,
                            "decision_date": application_date}
            except AttributeError:
                pass
            counter += 1
        return _dict


    tree = etree.parse(input_filename)
    root = tree.getroot()
    contracts = tree.xpath("//Application/contract")
    dict_of_clients = get_overdue_contracts(contracts)
    create_xml_2(dict_of_clients)
make_decisions("task1.xml")

