class Promptlibrary:
    def __init__(self,ticket_header,ticket_details,attachment=None):
        self.ticket_header = ticket_header
        self.ticket_details = ticket_details
        self.attachment = attachment

    def get_prompt_from_ticketDetails(self):
        prompt = f"""
            You are given the content of an email, including both the header and body. 
            Your task is to extract the invoice number from the provided text.

            The invoice number may appear in the subject line, header, or body of the email.

            Only return the invoice number itself, without additional words, labels, or formatting.

            If no invoice number is present, return null.

            Header: {self.ticket_header}
            Body: {self.ticket_details}
            """
        return prompt

    def get_invoice_number_from_attachment_pdf(self,invoice_text):
        prompt = f"""
                You are an AI assistant that specializes in reading and extracting structured data from business documents such as invoices.

                I will provide you with an invoice (either in text form or as OCR-processed content). Your task is to carefully analyze the invoice and extract the following information:

                1. **Invoice Number** – This may appear as "Invoice No.", "Invoice #", "Inv No.", or similar variations. Extract the exact value as written on the document. Do not infer or guess.

                

                ### Important Instructions:
                - If multiple numbers are present, choose the one explicitly labeled as "Invoice" or "Order/Purchase Order".
                - If the required number cannot be found, return "Not Found" instead of guessing.
                

                

                Here is the invoice content to analyze:

            {invoice_text}
                """
        return prompt


    def get_order_number_from_attachment_pdf(self,invoice_text):
        prompt = f"""
                You are an AI assistant that specializes in reading and extracting structured data from business documents such as invoices.

                I will provide you with an invoice (either in text form or as OCR-processed content). Your task is to carefully analyze the invoice and extract the following information:

                1. **Order Number** – This may appear as "Order No.","Buyer's Order No.", "Order ID", "PO Number", "Purchase Order", or similar terms. Extract the exact value as written on the document. Do not infer or guess.

                

                ### Important Instructions:
                - If multiple numbers are present, choose the one explicitly labeled as "Order No.","Buyer's Order No."
                - If the required number cannot be found, return "Not Found" instead of guessing.
                

                

                Here is the invoice content to analyze:

            {invoice_text}
                """
        return prompt