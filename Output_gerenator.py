from datetime import datetime

def out_gen(results_vuln,name):
    Page_content = """
    <html>
    <head>
    <style>
    #customers {
    font-family: Arial, Helvetica, sans-serif;
    border-collapse: collapse;
    width: 100%;
    }
    #customers td, #customers th {
    border: 1px solid #ddd;
    padding: 8px;
    }
    #customers tr:nth-child(even){background-color: #f2f2f2;}
    #customers tr:hover {background-color: #ddd;}
    #customers th {
    padding-top: 12px;
    padding-bottom: 12px;
    text-align: left;
    background-color: #04AA6D;
    color: white;
    }
    </style>
    </style>
    <body>
    <table id="customers">
    <tr>
    <th>Serverity</th>
	<th>Vendoe, product</th>
	<th>Description</th>
	<th>Date</th>
	<th>CVSS</th>
	<th>CVE</th>
	<th>Link</th>
	</tr>
    """
    str_tail = """
    </table>
    <body>
    </html>
    """
    for x in results_vuln:
        tmp_str = "<tr>"
        for i in x:
            if i == "Severity":
                i = "Not Assigend"
            tmp_str = tmp_str + "<td>{}</td>".format(i)
        tmp_str = tmp_str +"</tr>"
        Page_content = Page_content + tmp_str
    Page_content = Page_content + str_tail
    out_file = open("outputs/{}.html".format(name),'w')
    out_file.write(Page_content)
    out_file.close()
    print("{t},\t{n}.html Generated successfilly".format(t=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),n=name))