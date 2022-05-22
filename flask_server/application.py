from flask import Flask, request, render_template, redirect, jsonify, send_file
from datetime import datetime
from flask_mysqldb import MySQL
from cryptography.fernet import Fernet
from flask_socketio import SocketIO, emit
import yaml, os
from basic_routes import blueprint
from werkzeug.utils import secure_filename
import random, os, shutil
import string


# from user_manager import test_blueprint

########################################################################################################################
############################################### Main Backend Logic #####################################################
''' --- Defines the routes for the web application. Also sends database queries and delivers answer to Frontend. --- '''
########################################################################################################################
########################################################################################################################

# @Author David Witek
#logging file is saved in flask_server/record.log
#logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

# Secret key is needed for encryption.
application = Flask(__name__)
application.config['SECRET_KEY'] = 'mysecret'

# create cryptographer and insert key for encryption
# @Author David Witek
file = open('key.key', 'rb')
key = file.read()
file.close()
cryptographer = Fernet(key)

#### Register blueprint from basic_routes.py to outsource routes####
# @Author David Witek                                                                 #
application.register_blueprint(blueprint)
#                                                                  #
####################################################################

# Setup MySQL database configuration for DB connections.
mysql = MySQL(application)
db = yaml.load(open('db_config.yaml'))
application.config['MYSQL_HOST'] = db['mysql_host']
application.config['MYSQL_USER'] = db['mysql_user']
application.config['MYSQL_PASSWORD'] = db['mysql_password']
application.config['MYSQL_DB'] = db['mysql_db']

# Enable Cross-Origin Resource Sharing (CORS) Requests.
# Needed for communication between web server (HTTPS)
# and web socket server (WSS). They both run on different main routes,
# e. g. https://fulda-house-agency/ <--> wss://fulda-house-agency/socket.io/
socket_ = SocketIO(application, cors_allowed_origins="*", async_mode=None)
users = {}

# ---------------------------------------------------------------------------------------------------------------------#
# --------------------------------------- CHAT BOT INITIALIZATION & TRAINING ------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------- @author Oliver Kovarna ------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#

import chatbot.chatbot

###################################### HELPER FUNCTION #############################################
''' --- Helper function: 'add_double_quotes_to_list_items' takes a list of strings and makes sure 
                         all list items are surrounded by double quotes for valid JSON format. --- '''
# @author Oliver Kovarna
####################################################################################################
def add_double_quotes_to_list_items(string_list):
    temp_list = '['
    for i in range(0, len(string_list) - 1):
        temp_list += '"' + string_list[i] + '", '
    temp_list += '"' + string_list[len(string_list) - 1] + '"]'
    return temp_list

###################################### HELPER FUNCTION #############################################
''' --- Helper function: 'write_to_json' appends new objects containing tag, patterns and 
                         responses. --- '''

# @author Oliver Kovarna
####################################################################################################
def write_to_json(name, tag, patterns, responses):
    temp = open('./chatbot/temp', 'wb')
    with open('./chatbot/job_intents.json', 'r') as fin:
        for line in fin:
            lineStrip = line.strip() + '\n'
            if lineStrip == '}\n':
                next_line = next(fin).strip() + '\n'
                if next_line == ']\n':
                    temp.write(bytes('    },\n', encoding='utf8'))
                    temp.write(bytes('    {\n', encoding='utf8'))
                    if name != '':
                        temp.write(bytes('      "tag": "' + name + ' ' + tag + '",\n', encoding='utf8'))
                    else:
                        temp.write(bytes('      "tag": "' + tag + '",\n', encoding='utf8'))
                    temp.write(bytes('      "patterns": ' + add_double_quotes_to_list_items(patterns) + ',\n', encoding='utf8'))
                    temp.write(bytes('      "responses": ' + add_double_quotes_to_list_items(responses) + '\n', encoding='utf8'))
                    temp.write(bytes('    }\n', encoding='utf8'))
                    temp.write(bytes('  ]\n', encoding='utf8'))
                    temp.write(bytes('}', encoding='utf8'))
                    break
            temp.write(bytes(line, encoding='utf8'))
    temp.close()
    shutil.move('./chatbot/temp', './chatbot/job_intents.json')

###################################### HELPER FUNCTION #############################################
''' --- Helper function: 'save_all_properties' adds the tag 'property list' with certain patterns 
                         and responses. --- '''

# @author Oliver Kovarna
####################################################################################################
def save_all_properties(properties):
    property_name_list = ''
    for j in range(0, len(properties) - 1):
        property_name_list += properties[j][0] + ', '
    property_name_list += properties[len(properties) - 1][0] + '.'

    patterns = ["What properties are available",
                "What properties are for sale",
                "Tell me what properties are available",
                "Tell me what properties are for sale",
                "Give me a list of all properties"]
    responses = [property_name_list]

    write_to_json('', 'property list', patterns, responses)

###################################### HELPER FUNCTION #############################################
''' --- Helper function: 'initialize_chat_bot_data' creates all training data (JSON) for the chat 
                         bot. It calls two helper functions that create further training data. --- '''

# @author Oliver Kovarna
####################################################################################################
def initialize_chat_bot_data():
    with application.app_context():
        cur = mysql.connection.cursor()
        cur.execute("SELECT name, price, square_meter, rooms, city, zipcode, street, street_nr FROM properties " \
                    "WHERE price IS NOT NULL AND square_meter IS NOT NULL AND rooms IS NOT NULL AND city IS NOT NULL " \
                    "AND zipcode IS NOT NULL AND street IS NOT NULL AND street_nr IS NOT NULL AND is_deleted = 0 " \
                    "AND sold = 0 AND approved = 1")
        property_rows = cur.fetchall()
        mysql.connection.commit()
        cur.close()

        for i in range(0, len(property_rows)):
            name = property_rows[i][0]

            price = property_rows[i][1]
            patterns = ["How much is " + name,
                        "Tell me the price of " + name,
                        "How much costs " + name,
                        "How expensive is " + name]
            responses = ["The property " + name + " costs " + str(price) + " €.",
                         "It costs " + str(price) + " €.",
                         "The current price is " + str(price) + " €."]

            write_to_json(name, 'price', patterns, responses)

            squareMeters = property_rows[i][2]
            patterns = ["How many square meters has " + name,
                        "Tell me the square meters of " + name]
            responses = ["The property " + name + " has " + str(squareMeters) + " square meters.",
                         "It has " + str(squareMeters) + " square meters."]

            write_to_json(name, 'square meters',  patterns, responses)

            rooms = property_rows[i][3]
            patterns = ["How many rooms has " + name,
                        "Tell me the number of rooms for " + name]
            responses = ["The property " + name + " has " + str(rooms) + " rooms.",
                         "It has " + str(rooms) + " rooms."]

            write_to_json(name, 'rooms', patterns, responses)

            city = property_rows[i][4]
            patterns = ["Where is " + name,
                        "Tell me the location of " + name]
            responses = ["The property " + name + " is in " + city + ".",
                         "It is in " + city + "."]

            write_to_json(name, 'city', patterns, responses)

            zipcode = property_rows[i][5]
            patterns = ["What is the zipcode of " + name,
                        "Tell me the zipcode of " + name]
            responses = ["The property " + name + " has the zipcode " + str(zipcode) + ".",
                         "It has the zipcode " + str(zipcode) + "."]

            write_to_json(name, 'zipcode', patterns, responses)

            street = property_rows[i][6]
            patterns = ["In which street is " + name,
                        "Tell me the street name of " + name]
            responses = ["The property " + name + " is in the street " + street + ".",
                         "It is in the street " + street + "."]

            write_to_json(name, 'street', patterns, responses)

            street_nr = property_rows[i][7]
            patterns = ["What is the street number of " + name,
                        "Tell me the street number of " + name]
            responses = ["The property " + name + " has the street number " + str(street_nr) + ".",
                         "It has the street number " + str(street_nr) + "."]

            write_to_json(name, 'street number', patterns, responses)

            patterns = ["What can you tell me about " + name,
                        "Tell me about " + name, "What about " + name,
                        "What do you know about " + name,
                        "Tell me more about " + name,
                        "What can you tell me about " + name,
                        "Tell me about " + name,
                        "What about " + name,
                        "What do you know about " + name,
                        "Tell me more about " + name]
            responses = ["The property " + name + " costs " + str(price) + " €.",
                         "It costs " + str(price) + " €.",
                         "The current price is " + str(price) + " €.",
                         "The property " + name + " has " + str(squareMeters) + " square meters.",
                         "It has " + str(squareMeters) + " square meters.",
                         "The property " + name + " has " + str(rooms) + " rooms.",
                         "It has " + str(rooms) + " rooms.",
                         "The property " + name + " is in " + city + ".",
                         "It is in " + city + ".",
                         "The property " + name + " has the zipcode " + str(zipcode) + ".",
                         "It has the zipcode " + str(zipcode) + ".",
                         "The property " + name + " is in the street " + street + ".",
                         "It is in the street " + street + ".",
                         "The property " + name + " has the street number " + str(street_nr) + ".",
                         "It has the street number " + str(street_nr) + "."]

            write_to_json(name, 'random', patterns, responses)

            patterns = ["Tell me everything about " + name,
                        "Give me all information about " + name,
                        "List all information about " + name,
                        "How much do you know about " + name,
                        "What is interesting about " + name]
            responses = ["The property " + name + " costs " + str(price) + " €. "
                         + name + " has " + str(squareMeters) + " square meters. "
                         + "It has " + str(rooms) + " rooms. "
                         + "The property " + name + " is located in " + city + ". "
                         + "The zipcode of " + name + " is " + str(zipcode) + ". "
                         + "It is in the street " + street + " with the street number " + str(street_nr) + "."]

            write_to_json(name, 'general', patterns, responses)

    save_all_properties(property_rows)

############################### CHECK ON APPLICATION START UP ######################################
''' --- Check if all chat bot related files have already been created to avoid multiple chat bot 
        initialization and training.. --- '''


# @author Oliver Kovarna
####################################################################################################
if not os.path.exists('./chatbot/chatbot_model.h5') and not os.path.exists('./chatbot/lemmas.pkl') \
        and not os.path.exists('./chatbot/classes.pkl'):
    print('INITIALIZE CHAT BOT DATA')
    initialize_chat_bot_data()
    print('DONE WITH CHAT BOT INITIALIZATION')
    print('TRAIN CHAT BOT ON DB DATA')
    chatbot.chatbot.train_model()
    print('DONE WITH CHAT BOT TRAINING ON DB DATA')
else:
    print('CHAT BOT IS ALREADY TRAINED ON DB DATA')

import chatbot.processor

# ---------------------------------------------------------------------------------------------------------------------#
# ------------------------------------------------- REST API ----------------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#

# ----------------------------------------------------- ROUTING -------------------------------------------------------#

###################################### Route to main page ###########################################
''' --- Sets the route to the main page. Main pages look differently according to the user's 
        role --- '''
# @author David Witek
#####################################################################################################
@application.route('/user/id/<userId>', methods=['GET'])
def render_main_page(userId):
    result = execute_query('SELECT is_agent, is_manager FROM participant WHERE ParticipantId = %s', userId)
    if result[0][0] == 1:
        print("logged in as agent!")
        return render_template('Main/main_agent.html')
    elif result[0][1] == 1:
        print("logged in as manager!")
        return render_template('Main/main_manager.html')
    else:
        print("logged in as customer!")
        return render_template('Main/main_customer.html')




# ------------------------------------------------- DB QUERIES -------------------------------------------------------#
#--------- Start HOUSEMATCH HOUSEMATCH HOUSEMATCH HOUSEMATCH HOUSEMATCH HOUSEMATCH HOUSEMATCH HOUSEMATCH HOUSEMATCH Start --------#

###################################### Get Housematch Hashtags ###########################################
''' --------- Selects all properties from the database that are marked with matching hashtags -------- '''
###################################### Created by Joshua and Elisabeth ###################################
@application.route('/user/id/<userId>/hm-result', methods=['POST'])
def get_hm_results(userId):
    dataObj = request.get_json()
    checked_hashtags = dataObj.get("hts")       # holds ids and names of checked hashtags
    nr_hts = dataObj.get("len")
    # print("nr_hts = ", nr_hts)
    # print("checked HTs = ", checked_hashtags)
    hashtag_ids = [];                           # will hold ids of checked hashtags

    '''
    query = "SELECT properties.name, housematch_hashtag.hashtag_name FROM test_db.property_and_hashtag"  \
            " INNER JOIN  test_db.properties"  \
            " on test_db.properties.property_id = property_id_fk_2"  \
            " INNER JOIN test_db.housematch_hashtag"  \
            " on test_db.housematch_hashtag.housematch_hashtag_id= housematch_hashtag_id_fk" \
            " WHERE"
    '''

    # query to select the ids of the properties that are marked with matching hashtags
    # counts how many hashtags apply to request
    query = "SELECT COUNT(property_id) as count, properties.property_id FROM test_db.property_and_hashtag" \
            " INNER JOIN test_db.properties on test_db.properties.property_id = property_id_fk_2" \
            " INNER JOIN test_db.housematch_hashtag on test_db.housematch_hashtag.housematch_hashtag_id = housematch_hashtag_id_fk" \
            " WHERE"

    # extend query to all chosen hashtags
    for hashtag in checked_hashtags:
        query += " housematch_hashtag_id_fk = " + str(hashtag[0]) + " and test_db.properties.approved = 1 and test_db.properties.sold = 0 and test_db.properties.is_deleted = 0 or"
        hashtag_ids.append(hashtag[0])              # save only the id of the hashtags for later

    # delete the last ' or' in query (otherwise there will be a syntax error)
    query = query[0:len(query)-3]
    query += " GROUP BY(property_Id)"
    print("query = ", query)

    results = execute_query(query)          # all properties that are linked to at least one matching hashtag
    print("matching properties are = ", results)

    match = []          # one row of match holds the id of the current property + the matching percentage
    match_dict = {}
    # loop through all matching properties (all properties that have at least 1 wanted hashtag linked to them)
    for prop in results:
        # prop[0] = count
        # prop[1] = id of current property

        # query to select all hashtags that are linked to the current property
        query2 = 'SELECT housematch_hashtag_id_fk from test_db.property_and_hashtag WHERE property_id_fk_2 = ' + str(prop[1])
        zw_res = execute_query(query2)                  # all hashtags of the current property
        all_hts_of_prop = str(zw_res)                   # all hashtags of the current property as a string
        nr_hts_in_db = len(zw_res)                      # number of hashtags of the current property
        # print("Prop nr hts in db = ", nr_hts_in_db)
        #print("all HTs of the current property = ", all_hts_of_prop)
        #print("asked hts = ", hashtag_ids)

        # variable that counts how many of the wanted hashtags are actually linked to the current property
        count = 0
        # loop through all the wanted hashtags
        for ht_id in hashtag_ids:
            # if the wanted hashtag is also linked to the current property: increase count
            if str(ht_id) in str(all_hts_of_prop):
                count += 1
                # print(str(ht_id) + " is in all_hts_of_prop")
        #("number of asked HTs that are also linked HTs = ", count)

        # calculate how many per cent of the wanted hashtags are linked to the current property
        perc = round(float((count/len(hashtag_ids)) * 100), 2)
        # print("percentage of (" + str(count) + " / " + str(len(hashtag_ids)) + "* 100) = ", perc)

        # make sure that no property gets more than 100 %
        if perc >= 100:
            perc = 100

        # match holds the id of the current property + the matching percentage
        # res_string = str(prop[1]) + ": " + str(perc)
        # match[str(prop[1])] = perc
        match_dict[str(prop[1])] = perc
        match.append([prop[1], perc])

    print("match array = ", match)

    # return resulting ids + percentage to frontend

    return jsonify(match)

########################################## Helper method ############################################
''' --- Selects all properties with details from the properties table that match the Housematch
        hashtags defined by the user. --- '''
######################################### Created by Elisabeth ######################################
@application.route('/user/id/<userId>/hm-result-properties', methods=['POST'])
def get_HM_properties(userId):
    dataObj = request.get_json()
    print("dataObj hm-result-props = ", dataObj)
    ids = dataObj.get('prop_ids')       # holds the ids of the correct properties

    # query to select the details of the properties
    if len(ids) > 0:
        query = "SELECT * FROM properties WHERE"
        for id in ids:
             query += " property_id = " + str(id) + " and test_db.properties.approved = 1 and test_db.properties.sold = 0 and test_db.properties.is_deleted = 0 or"
        # delete the last ' or' in query (otherwise there will be a syntax error)
        query = query[0:len(query)-3]
       # query += " and test_db.properties.approved = 1 and test_db.properties.sold = 0 and test_db.properties.is_deleted = 0"
        query += " ORDER BY property_id ASC"    # important so the order is the same as the percentages for frontend
        print("Query = ", query)
        properties = execute_query(query)       # resulting array from database (holds details of properties)
        #print(properties)
        if len(properties) == 0:
            properties = "No properties found"
            print("No new properties")
        print("result in get_hm_properties", properties)
        return jsonify(properties)              # return properties to frontend
    else:
        return "No Properties found"


############################################# Add HTs ###############################################
''' --- Link HTs to certain property --- '''
#####################################################################################################
@application.route('/user/id/<userId>/hm-hashtags', methods=['POST'])
def add_hm_hashtags(userId):
    dataObj = request.get_json()
    # print("dataObj = ", dataObj)
    id = dataObj.get('propId')          # property to link HTs to
    hashtags = dataObj.get('hts')       # holds the chosen hashtags
    # print("id = ", id)
    # print("hts = ", hashtags)

    # TODO make sure that the same hashtag cannot be linked to the same property more than once

    # insert a new row for every hashtag that should be linked to property
    # TODO possible without execute_query every single time with INSERT statement for multiple rows?
    # see also: link_new_hts()
    for hashtag in hashtags:
        query = 'INSERT into test_db.property_and_hashtag (property_id_fk_2, housematch_hashtag_id_fk)' \
                ' VALUES(%s, %s)'
        execute_query(query, id, hashtag)

    return jsonify("Inserted new hashtags")

######################################### Get linked HTs ############################################
''' --- Selects all hashtags linked to a certain property in the database --- '''
######################################### Created by Elisabeth ######################################
@application.route('/user/id/<userId>/property-hashtags', methods=['POST'])
def get_linked_hts(userId):
    dataObj = request.get_json()
    propId = dataObj.get('propId')
    # print("propId in get linked hts = ", propId)

    # query gets all hashtag ids linked to a certain property id (table: property_and_hashtag)
    # and then gets the names of the hashtags to display them for the user (table: housematch_hashtag)
    query = "SELECT  test_db.housematch_hashtag.hashtag_name" \
            " from test_db.property_and_hashtag" \
            " INNER JOIN test_db.housematch_hashtag" \
            " on  housematch_hashtag_id = housematch_hashtag_id_fk" \
            " WHERE property_id_fk_2 = " + str(propId)

    # print("Linked HTs query = ", query)

    result = execute_query(query)

    # returns names of the linked hashtags or 'None'
    if len(result) > 0:
        return jsonify(result)
    else:
        return "None"

########################################## link new HTs #############################################
''' --- Updates the database table for hashtags linked to properties --- '''
######################################### Created by Elisabeth ######################################
@application.route('/user/id/<userId>/new-property-hashtags', methods=['POST'])
def link_new_hts(userId):
    dataObj = request.get_json()
    propId = dataObj.get('propId')
    new_hts = dataObj.get('hts')
    # print("new hts = ", new_hts)

    # delete all existing hashtags linked to property from database
    query1 = "DELETE FROM test_db.property_and_hashtag WHERE property_id_fk_2 = " + str(propId)
    execute_query(query1)

    # insert new hashtags
    query2 = "INSERT INTO test_db.property_and_hashtag (property_id_fk_2, housematch_hashtag_id_fk) VALUES "
    # how to add multiple rows to db: VALUES (1, 1), (1, 2), (1, 3);
    for ht in new_hts:
        query2 += "(" + str(propId) + ", " + str(ht) + "),"

    # delete redundant last comma
    query2 = query2[0:len(query2)-1] + ";"
    # print("New hts query = ", query2)

    execute_query(query2)

    return "Added new HTs to property"

#--------- End HOUSEMATCH HOUSEMATCH HOUSEMATCH HOUSEMATCH HOUSEMATCH HOUSEMATCH HOUSEMATCH HOUSEMATCH HOUSEMATCH End --------#

############################################# GET ###################################################
''' --- --- '''
#####################################################################################################
@application.route('/not-deleted-flagged-properties', methods=['GET'])
def get_not_deleted_flagged_properties():
    properties = execute_query('SELECT * FROM properties WHERE is_deleted != 1 ORDER BY name ASC')
    return jsonify(properties)

############################################# GET ###################################################
''' ---         Sends GET request to DB to retrieve a single property with a certain Id.      --- '''
#####################################################################################################
@application.route('/get-single-property/<propId>', methods=['GET'])
def get_single_property(propId):
    id = int(propId)
    query = "SELECT properties.*, GROUP_CONCAT(housematch_hashtag.hashtag_name SEPARATOR ', ' ) as Hashtags FROM test_db.property_and_hashtag " \
            " INNER JOIN  test_db.properties" \
            " on test_db.properties.property_id = property_id_fk_2" \
            " INNER JOIN test_db.housematch_hashtag" \
            " on test_db.housematch_hashtag.housematch_hashtag_id= housematch_hashtag_id_fk" \
            " WHERE property_id = %s" \
            " GROUP BY name ORDER BY property_id;"
    print(query)
    property = execute_query(query, id)
    return jsonify(property)

############################################# GET ###################################################
''' --- Sends GET request to DB to retrieve all customers.  --- '''
# @Author David Witek and Darya Traxel
#####################################################################################################
@application.route('/get-all-customers', methods=['GET'])
def get_all_customers():
    customers = execute_query('SELECT * FROM participant WHERE is_agent <> 1 and  is_manager <> 1 and is_disabled = false ORDER BY Username ASC')

    all_customers = []
    customer_data = []
    # convert the response tuple to  list to be able to modify values
    for customer in customers:
        for data in customer:
            customer_data.append(data)
        all_customers.append(customer_data)
        customer_data = []

    # iterate over the newly created list and decrypt the password
    for customer in all_customers:
        password = cryptographer.decrypt(customer[2].encode()).decode('utf-8')
        customer[2] = password


    return jsonify(all_customers)



############################################# GET ###################################################
''' --- Sends GET request to DB to retrieve all hashtags.  --- '''
#####################################################################################################
@application.route('/get-all-hashtags', methods=['GET'])
def get_all_hashtags():
    hashtags = execute_query('SELECT * FROM housematch_hashtag ORDER BY housematch_hashtag_id ASC')
    return jsonify(hashtags)

############################################# GET ###################################################
''' --- Sends GET request to DB to retrieve all users.  --- '''
#####################################################################################################
###################################### Created by Joshua and David ##################################
@application.route('/get-all-users', methods=['GET'])
def get_all_users():
    users = execute_query('SELECT * FROM participant INNER JOIN agency ON participant.agency_fk = agency.agency_id ORDER BY Username ASC')

    list_of_all_users = []
    user_data = []
    # convert the response tuple to  list to be able to modify values
    for user in users:
        for data in user:
            user_data.append(data)
        list_of_all_users.append(user_data)
        user_data = []

    # iterate over the newly created list and decrypt the password
    for user in list_of_all_users:
        password = cryptographer.decrypt(user[2].encode()).decode('utf-8')
        user[2] = password

    return jsonify(list_of_all_users)


############################################# GET ###################################################
''' --- Sends GET request to DB to retrieve data from a certain user. Data will be used to
        render user's profile. --- '''
#####################################################################################################
@application.route('/getProfile/<userId>', methods=['GET'])
def get_profile(userId):
    profile = execute_query('SELECT * FROM participant INNER JOIN agency ON participant.agency_fk = agency.agency_id WHERE ParticipantId = %s ', userId)
    return jsonify(profile)




############################################# POST #################################################
''' --- Updates the DB entry for a password of a certain user. Only BMs can change passwords --- '''
####################################################################################################
###################################### Created by Joshua and David #################################
# TODO change to PUT
@application.route('/changePassword', methods=['POST'])
def changePassword():
    dataObj = request.get_json()
    userid = dataObj.get('userid')
    password = ''
    for i in range(6):
        password = password + str(random.randint(1, 9)) + str(random.choice(string.ascii_letters))

    encrypted_password = cryptographer.encrypt(password.encode())

    execute_query('Update participant SET Password = %s WHERE ParticipantId = %s', encrypted_password, userid)
    return jsonify("Password was changed")


###################################### Created by Darya ###########################################
@application.route('/changeStatus', methods=['PUT'])
def changeStatus():
    statusObj = request.get_json()
    userid = statusObj.get('userid')
    print('userId: ', userid)
    execute_query('UPDATE participant SET is_legitimate = True WHERE ParticipantId = %s', userid)
    return jsonify("Status has changed")

###################################### Created by Darya ###########################################
@application.route('/changeAccess', methods=['PUT'])
def changeAccess():
    statusObj = request.get_json()
    userid = statusObj.get('userid')
    print('userId: ', userid)
    alreadyDisabled = execute_query('SELECT ParticipantId, is_disabled FROM participant  WHERE ParticipantId = %s AND is_disabled = True', userid)
    if len(alreadyDisabled) > 0:
        execute_query('UPDATE participant SET is_disabled = False WHERE ParticipantId = %s', userid)
    else:
        execute_query('UPDATE participant SET is_disabled = True WHERE ParticipantId = %s', userid)
    return jsonify("Access has changed")

############################################# POST #################################################
''' --- Updates the DB entry for a first and last name of a certain user. Every user can change his
        or her name. --- '''
####################################################################################################
# TODO change to PUT
@application.route('/change-profile/<userId>', methods=['POST'])
def change_profile(userId):
    profileObj = request.get_json()
    fname = profileObj.get('fname')
    lname = profileObj.get('lname')

    query = "UPDATE participant SET firstname = %s, " \
            "lastname = %s " \
            "WHERE ParticipantId = %s"

    execute_query(query, fname, lname, userId)
    return jsonify("updated userprofile")

############################################# POST #################################################
''' --- Updates the DB entry for a first and last name of a certain user. Every user can change his
        or her name. --- '''
# @Author David Witek and Elisabeth Milde
####################################################################################################
@application.route('/change-profile-agent/<userId>', methods=['POST'])
def change_profile_agent(userId):
    profileObj = request.get_json()
    fname = profileObj.get('fname')
    lname = profileObj.get('lname')
    agency = profileObj.get('agencyName')

    old_user_data = execute_query("SELECT participant.firstname, participant.lastname, agency.name FROM participant INNER JOIN agency ON participant.agency_fk = agency.agency_id WHERE ParticipantId = %s", userId)
    print(old_user_data)
    if fname:
        fname = fname.strip()
    else:
        fname = old_user_data[0][0]
    if lname:
        lname = lname.strip()
    else:
        lname = old_user_data[0][1]
    if agency:
        agency = agency.strip()
    else:
        agency = old_user_data[0][2]

    result = execute_query("SELECT agency_id FROM agency WHERE name = %s", agency)

    if result:
        is_old_agency = True
        agency_id = result[0][0]
    else:
        is_old_agency = False

    if is_old_agency:
        execute_query("UPDATE participant SET firstname = %s, lastname = %s, agency_fk = %s WHERE ParticipantId = %s", fname, lname, agency_id, userId)
    else:
        execute_query("INSERT INTO agency (name) VALUES (%s)", agency)
        result = execute_query("SELECT agency_id FROM agency WHERE name = %s", agency)
        agency_id = result[0][0]
        execute_query("UPDATE participant SET firstname = %s, lastname = %s, agency_fk = %s WHERE ParticipantId = %s", fname, lname, agency_id, userId)

    return jsonify("updated userprofile")

############################################# POST #################################################
''' --- Retrieves all properties which satisfy the user's search term and filter criteria. The user
        can filter for the maximal price, number of rooms and square meters. The search term can be
        any string <= 40 characters. It will be tested against the name and the location of the 
        property. --- '''
# @Author David Witek and Elisabeth Milde
####################################################################################################
# creates the DB query depending on given searchword and filtercriterias
@application.route('/user/id/<userId>/search', methods=['POST'])
def search_term_in_db(userId):

    # retrieve all data from POST
    dataObj = request.get_json()
    search_term = dataObj.get('search_term')
    max_price = dataObj.get('maxP')
    max_rooms = dataObj.get('maxR')
    max_square_meters = dataObj.get('maxS')
    sold_checkbox = dataObj.get('sold_checkbox')
    my_listing_checkbox = dataObj.get('my_listing_checkbox')
    pending_checkbox = dataObj.get('pending_checkbox')
    is_customer = dataObj.get('is_customer')
    print("is_customer: ", is_customer)

    # define the beginning of the SQL query
    search_query = "SELECT * FROM properties"

    # flag to determine if any of the basic filters have been applied to adjust the following filters with 'and'
    flag = False

    # array to store all parameters that will be used in the SQL query later on
    arr_filter_data = []

    #######################################################################################
    # Here the search query for the basic filter that the customer can use is being built #
    #######################################################################################

    # checks if searchword input was given if not query string is empty
    print("search term: ",search_term)
    if search_term is None:
        search_term_query = ""
    elif len(search_term) > 40:
        return "Searchword is too long!"
    else:
        # if searchword is not empty create a string for the query and add the parameter to an array for later use
        search_term_query = " WHERE (name LIKE '{}' or city LIKE '{}')"
        # add % for LIKE search in SQL
        search_term = "%" + search_term + "%"
        # append parameters twice because of query above
        arr_filter_data.append(search_term)
        arr_filter_data.append(search_term)
        # set flag to True to signal that the following query parts have to be concatenated via AND
        flag = True
        # following if statements are identical in function to the first if statement

    if max_price == 0:
        price_query = ""
    else:
        if flag:
            price_query = " AND price <= {}"
        else:
            price_query = " WHERE price <= {}"

        arr_filter_data.append(max_price)
        flag = True

    if max_rooms == 0:
        rooms_query = ""
    else:
        if flag:
            rooms_query = " AND rooms <= {}"
        else:
            rooms_query = " WHERE rooms <= {}"

        arr_filter_data.append(max_rooms)
        flag = True

    if max_square_meters == 0:
        square_meter_query = ""
    else:
        if flag:
            square_meter_query = " AND square_meter <= {}"
        else:
            square_meter_query = " WHERE square_meter <= {}"

        arr_filter_data.append(max_square_meters)
        flag = True


    #############################################################################################
    # here the checkboxes of the agent and manager are checked and added to the query if needed #
    #############################################################################################

    # checks if sold checkbox was selected
    if sold_checkbox:
        if flag:
            sold_checkbox_query = ' AND sold = 1'
        else:
            sold_checkbox_query = ' WHERE sold = 1'
        flag = True
    else:
        sold_checkbox_query = ''

    # checks if my listings checkbox was selected
    if my_listing_checkbox:
        if flag:
            my_listing_checkbox_query = ' AND agent_id_fk = {}'
        else:
            my_listing_checkbox_query = ' WHERE agent_id_fk = {}'
        arr_filter_data.append(userId)
        flag = True
    else:
        my_listing_checkbox_query = ''

    # checks if pending checkbox was selected
    if pending_checkbox:
        if flag:
            pending_checkbox_query = ' AND approved = 0'
        else:
            pending_checkbox_query = ' WHERE approved = 0'
        flag = True
    else:
        pending_checkbox_query = ''

    # here the AND is being added to the customer query and the query end
    if flag:
        customer_filter = ' AND approved = 1 AND sold = 0'
        # add this part at the end of the query to order the results
        not_deleted_and_ordered = ' AND is_deleted != 1 ORDER BY name ASC;'
    else:
        customer_filter = ' WHERE approved = 1 AND sold = 0'
        not_deleted_and_ordered = ' WHERE is_deleted != 1 ORDER BY name ASC;'

    # checks if the requests is from the main_customer view if yes it only applies filter available to the customer
    if is_customer:
        not_deleted_and_ordered = ' AND is_deleted != 1 ORDER BY name ASC;'
        search_query += search_term_query + price_query + rooms_query + square_meter_query + customer_filter + not_deleted_and_ordered
    # else the query must be from an agent or manager so additional filter are being added to the query
    else:
        search_query += search_term_query + price_query + rooms_query + square_meter_query + sold_checkbox_query + my_listing_checkbox_query + pending_checkbox_query + not_deleted_and_ordered

    # insert all parameters saved in the array into the query
    query = search_query.format(*arr_filter_data)
    print("query: ", query)
    result = execute_query(query)

    # check if anything was found, return string if nothing was found
    if len(result) > 0:
        return jsonify(result)
    else:
        return jsonify("No properties found")

# clicked on "Logout"
############################################# GET ##################################################
''' --- Updates DB entry for a certain user if he logs out so he will be marked as offline. 
        Also redirects to login page after logout. --- '''
####################################################################################################
@application.route('/logout', methods=['GET', 'PUT'])
def render_logout():
    user_id = request.args.get('userId')
    execute_query("UPDATE participant SET IsActive = False WHERE ParticipantId = %s", user_id)
    socket_.emit('refreshed chat list', {
        'message': 'Set partner status offline...'
    }, broadcast=True)

    return redirect('/')

# register the user
############################################# POST #################################################
''' --- Registration of a new user: Enters a new user into the participant table of the DB. Users 
        have to give their first and last name as well as a password which they have to confirm by 
        entering it twice. --- '''
# @Author David Witek and Oliver Kovarna
####################################################################################################
@application.route('/registration', methods=['POST'])
def register_user():
    # retrive data from frontend
    user_obj = request.get_json()
    username = user_obj.get('userName')
    email = user_obj.get('email')
    password = user_obj.get('password')
    register_as_agent = user_obj.get('register_as_agent')

    # encrypt the password
    # first encode password into bytes then encrypt the bytes
    encrypted_password = cryptographer.encrypt(password.encode())

    # check if username or email is already in database
    rows = execute_query("SELECT * FROM participant WHERE username= %s  OR email= %s ", username, email)
    if len(rows) > 0:
        return 'Already part of db!'
    # checks if user wants to be registered as agent or customer
    if register_as_agent:
        execute_query("INSERT INTO participant(username, password, email, is_agent, agency_fk) VALUES(%s, %s, %s, %s, %s)", username, encrypted_password, email, 1, 1)
        return 'Added new agent to db!'
    else:
        # else add regular user (customer) to db
        execute_query("INSERT INTO participant(username, password, email) VALUES(%s, %s, %s)" ,username, encrypted_password, email)
    return 'Added new customer to db!'

############################################# POST #################################################
''' --- User login: Checks if given credentials of a user are correct. If so updates the user's DB
        entry so he will be shown as online. If not, sends feedback to user. --- '''
# @Author David Witek and Oliver Kovarna
####################################################################################################

@application.route('/login', methods=['POST'])
def login_user():
    # retrieve data from frontend
    user_obj = request.get_json()
    username = user_obj.get('userName')
    password = user_obj.get('password')

    # check how many users are currently active and check if user can login
    active_users = execute_query("SELECT IsActive FROM participant WHERE IsActive = 1")
    if len(active_users) > 50:
        return "Too many active users, try again later!"

    # look for the user in db with given username or email
    user_rows = execute_query("SELECT ParticipantId, is_agent, is_manager, password FROM participant WHERE (username= %s OR email= %s ) AND is_disabled = False AND is_chat_bot = 0", username, username)

    # check if there is a result
    if len(user_rows) > 0:
        user_id = user_rows[0][0]

        user_id_str = str(user_id)
        # decrypt the password
        db_password = cryptographer.decrypt(user_rows[0][3].encode()).decode('utf-8')
        # check if password matches, if yes log the user in
        if db_password == password:
            execute_query("UPDATE participant SET IsActive = True WHERE ParticipantId = %s", user_id_str)

            socket_.emit('refreshed chat list', {
                'message': 'Set partner status online...'
            }, broadcast=True)

            url = '/users/id/' + user_id_str
            redirect(url)
            return user_id_str

    return 'Sry, your email address or password may be wrong. Try again!'

#--------------------------------------------------------------------------------------------------#
#------------------------------------- CHAT ENDPOINTS ---------------------------------------------#
#--------------------------------------------------------------------------------------------------#
#--------------------------------- @author Oliver Kovarna -----------------------------------------#
#--------------------------------------------------------------------------------------------------#

############################################# GET ##################################################
''' --- Chat endpoint: The chat endpoint 'render_chat_page' renders the chat GUI 
                       for the client. --- '''
# @author Oliver Kovarna
####################################################################################################
# TODO describe what method does
@application.route('/user/id/<userId>/chat-gui', methods=['GET'])
def render_chat_page(userId):
    return render_template('Chat/chat.html')

############################################# GET ##################################################
''' --- Chat endpoint: 'get_chat' retrieves the messages of a certain chat of a specific user 
                       with its partner from the DB and sends it back to the client. --- '''
# @author Oliver Kovarna
####################################################################################################
@application.route('/user/id/<userId>/chat', methods=['GET'])
def get_chat(userId):
    user_id_str = str(userId)
    chat_partner_name = request.args.get('partner')

    user_rows = execute_query("SELECT ParticipantId FROM participant WHERE Username='" + chat_partner_name + "'")

    # only do stuff if the desired chat partner exists
    if len(user_rows) > 0:
        chat_partner_id_str = user_rows[0][0]
        # get messages from DB where chat partner A = user and chat partner B = desired partner or the other way around
        chatRows = execute_query("SELECT ChatId FROM chat WHERE (FirstChatParticipantIdFk= %s  AND SecondChatParticipantIdFk= %s ) XOR (FirstChatParticipantIdFk= %s  AND SecondChatParticipantIdFk= %s )",user_id_str, chat_partner_id_str, chat_partner_id_str, user_id_str)

        # check if there has already been a chat between the partners
        if len(chatRows) > 0:
            chat_id_str = chatRows[0][0]
            # get all already sent messages with metadata
            message_rows = execute_query("SELECT Content, Timestamp, ParticipantIdFk, IsNotification FROM message WHERE ChatIdFk= %s", chat_id_str)

            # check if the chat partners already sent messages
            if len(message_rows) > 0:
                # put messages into array to display them on html site later
                temp_list = message_rows
                message_list = []
                for i in range(0, len(temp_list)):
                    message_list.append(temp_list[i])

                # return all already sent messages
                return jsonify(message_list)

            # otherwise return helpful error message
            return 'No messages for specified chat found in db'

        return 'No chats for specified users found in db'

    return 'No such chat partner in db'

############################################# GET ##################################################
''' --- Chat endpoint: 'get_chat_notifications' retrieves all notified messages 
                       of a certain user and chat and returns the total count of 
                       these messages. --- '''
# @author Oliver Kovarna
####################################################################################################
@application.route('/user/id/<userId>/chat/notifications', methods=['GET'])
def get_chat_notifications(userId):
    chat_id_rows = execute_query("SELECT ChatId FROM chat WHERE FirstChatParticipantIdFk = %s  XOR SecondChatParticipantIdFk = %s", userId, userId)
    notification_count = 0

    if len(chat_id_rows) > 0:
        for i in range(0, len(chat_id_rows)):
            message_notification_rows = execute_query("SELECT IsNotification FROM message WHERE ChatIdFk = %s AND ParticipantIdFk != %s AND IsNotification = 1", chat_id_rows[i][0], userId)
            notification_count += len(message_notification_rows)

        if notification_count > 0:
            notification_obj = {
                'notificationCount': notification_count
            }
            return jsonify(notification_obj)

        return jsonify({
            'notificationCount': 0
        })

    return 'No chats for user with ID ' + str(userId) + ' found in db'


############################################# PUT ##################################################
''' --- Chat endpoint: 'update_message_notification_status' updates the status
                       of a user's messages for a certain chat. --- '''
# @author Oliver Kovarna
####################################################################################################
@application.route('/user/id/<userId>/chat/notification-status', methods=['PUT'])
def update_message_notification_status(userId):
    chat_partner_obj = request.get_json()
    chat_partner_name = chat_partner_obj.get('chatPartnerName')
    user_rows = execute_query("SELECT ParticipantId FROM participant WHERE Username= %s", chat_partner_name)

    if len(user_rows) > 0:
        chat_partner_id = user_rows[0][0]
        chat_rows = execute_query("SELECT ChatId FROM chat WHERE (FirstChatParticipantIdFk= %s  AND SecondChatParticipantIdFk= %s) XOR (FirstChatParticipantIdFk= %s  AND SecondChatParticipantIdFk= %s)", userId, chat_partner_id, chat_partner_id, userId)

        if len(chat_rows) > 0:
            chat_id = chat_rows[0][0]
            message_rows = execute_query("SELECT Content, Timestamp, ParticipantIdFk, IsNotification FROM message WHERE ChatIdFk= %s", chat_id)

            if len(message_rows) > 0:
                execute_query("UPDATE message SET IsNotification = 0 WHERE ChatIdFk= %s AND ParticipantIdFk= %s", chat_id, chat_partner_id)
                return 'Notification for chatId ' + str(chat_id) + ' messages set to 0 in db'

            return 'No messages for specified chat found in db'

        return 'No chats for specified users found in db'

    return 'No such chat partner in db'

############################################# POST #################################################
''' --- Chat endpoint: 'save_user_message' retrieves the message from the client
        and inserts it into the DB. --- '''
# @author Oliver Kovarna
####################################################################################################
# TODO describe what method does
@application.route('/user/id/<userId>/chat/message', methods=['POST'])
def save_user_message(userId):
    chat_obj = request.get_json()
    chat_partner = chat_obj.get('chatPartner')
    content = chat_obj.get('textMessage')
    user_rows = execute_query("SELECT ParticipantId FROM participant WHERE Username= %s", chat_partner)

    if len(user_rows) > 0:
        chat_partner_id = user_rows[0][0]
        chat_rows = execute_query("SELECT ChatId FROM chat WHERE (FirstChatParticipantIdFk = %s  AND SecondChatParticipantIdFk = %s) XOR (FirstChatParticipantIdFk = %s  AND SecondChatParticipantIdFk = %s)", userId, chat_partner_id, chat_partner_id, userId)

        if len(chat_rows) == 0:
            execute_query("INSERT INTO chat(FirstChatParticipantIdFk, SecondChatParticipantIdFk) VALUES(%s, %s)", userId, chat_partner_id)

        chat_id = chat_rows[0][0]
        execute_query("INSERT INTO message(ChatIdFk, ParticipantIdFk, Content, Timestamp, IsNotification) VALUES(%s, %s, %s, %s, %s)", chat_id, userId, content, datetime.now(), 1)

        # chatbot message handling
        chat_bot_status = get_chat_bot_message(chat_partner_id, chat_id, content)
        print(chat_bot_status)

        return jsonify(chat_obj)

    return 'No such chat partner in db'

###################################### HELPER FUNCTION #############################################
''' --- Helper function: 'get_chat_bot_message' checks if the specific chat
                         partner is the chat bot, triggers the prediction of the chat bot response
                         and inserts the response in the database. --- '''
# @author Oliver Kovarna
####################################################################################################
def get_chat_bot_message(chat_partner_id, chat_id, message):
    user_rows = execute_query("SELECT Username FROM participant WHERE ParticipantId = %s AND is_chat_bot = 1", chat_partner_id)

    if len(user_rows) > 0:
        bot_message = chatbot.processor.get_chatbot_response(message)
        execute_query("INSERT INTO message(ChatIdFk, ParticipantIdFk, Content, Timestamp, IsNotification) VALUES(%s, %s, %s, %s, %s)", chat_id, chat_partner_id, bot_message, datetime.now(), 1)
        return 'Chat bot has sent a message'

    return 'No chat bot is required'

############################################# GET ##################################################
''' --- Chat endpoint: 'get_chatpartners' retrieves all chats for a specific
        user and returns them to the client. --- '''
# @author Oliver Kovarna
####################################################################################################
@application.route('/user/id/<userId>/chats', methods=['GET'])
def get_chatpartners(userId):
    chat_rows = execute_query("SELECT ChatId, FirstChatParticipantIdFk, SecondChatParticipantIdFk FROM chat WHERE FirstChatParticipantIdFk= %s  XOR SecondChatParticipantIdFk= %s", userId, userId)

    if len(chat_rows) > 0:
        notification_count_rows = []
        for i in range(0, len(chat_rows)):
            notification_rows = execute_query("SELECT COUNT(IsNotification) AS MessageCount FROM message WHERE IsNotification = 1 AND ChatIdFk = %s AND ParticipantIdFk != %s",
                                        chat_rows[i][0], userId)
            notification_count = notification_rows[0][0]
            notification_count_rows.append(notification_count)

        chat_participants = []
        chat_participant_ids = chat_rows
        for i in range(0, len(chat_participant_ids)):
            notificationCounter = notification_count_rows[i]
            for j in range(1, len(chat_participant_ids[i])):
                if chat_participant_ids[i][j] != int(userId):
                    # Add "AND is_disabled != 1" for "deleting" chat user from list
                    result = execute_query("SELECT Username, IsActive, is_agent, is_manager, is_chat_bot FROM participant WHERE ParticipantId= %s", chat_participant_ids[i][j])
                    chat_participants.append(
                        {
                            'name': result[0][0],
                            'status': result[0][1],
                            'isAgent': result[0][2],
                            'isManager': result[0][3],
                            'isChatBot': result[0][4],
                            'notificationCount': notificationCounter
                        })
        return jsonify(chat_participants)
    return 'No chats found for userId: ' + userId

############################################# GET ##################################################
''' --- Chat endpoint: 'get_contacts' retrieves a requested chat partner username 
        for a specific user from the DB and creates a new chat with the partner if 
        no chat exists. --- '''

# @author Oliver Kovarna
####################################################################################################
@application.route('/user/id/<userId>/contacts', methods=['GET'])
def get_contacts(userId):
    search_input = request.args.get('search')
    contact_rows = execute_query("SELECT ParticipantId FROM participant WHERE Username= %s  AND ParticipantId != %s", search_input, str(userId))

    if len(contact_rows) > 0:
        contact_obj = contact_rows[0]
        contact_id = contact_obj[0]
        chat_rows = execute_query("SELECT ChatId FROM chat WHERE (FirstChatParticipantIdFk= %s  AND SecondChatParticipantIdFk= %s ) XOR (FirstChatParticipantIdFk= %s  AND SecondChatParticipantIdFk= %s )", str(userId), str(contact_id), str(contact_id), str(userId))

        if len(chat_rows) > 0:
            return 'chat already exists!'

        execute_query("INSERT INTO chat(FirstChatParticipantIdFk, SecondChatParticipantIdFk) VALUES(%s, %s)", str(userId), str(contact_id))
        return 'successfully added new chat'
    return jsonify([])

############################################# GET ##################################################
''' --- Chat endpoint: 'get_image' loads a standard image from the filesystem and
        sends it back to the client. It is used to display a profile picture in the chat GUI. --- '''

# @author Oliver Kovarna
####################################################################################################
@application.route('/image', methods=['GET'])
def get_image():
    filename = './static/images/main_customer/profile.png'
    return send_file(filename, mimetype='image/png')

############################################# DELETE ###############################################
''' --- 'delete_listing' removes a propery from the corresponding DB tables. --- '''

# @author Oliver Kovarna
####################################################################################################
@application.route('/listing-removal', methods=['DELETE'])
def delete_listing():
    property_id = request.args.get('propertyId')
    query = "SELECT * FROM properties WHERE property_id = %s"
    listing_rows = execute_query(query, property_id)

    if len(listing_rows) > 0:

        query = "UPDATE properties SET is_deleted = 1 WHERE property_Id = %s"
        execute_query(query, property_id)

        return 'success'
    else:
        return 'failure'

############################################# PUT ##################################################
''' --- Updates the data of a specific property in the DB  --- '''
####################################################################################################
@application.route('/listing-update/<propId>', methods=['PUT'])
def update_listing(propId):
    listingObj = request.get_json()
    listingName = listingObj.get('listingName')
    listingPrice = listingObj.get('listingPrice')
    listingSqm = listingObj.get('listingSqm')
    listingRooms = listingObj.get('listingRooms')
    listingZip = listingObj.get('listingZip')
    listingCity = listingObj.get('listingCity')
    listingStreet = listingObj.get('listingStreet')
    listingStreetNo = listingObj.get('listingStreetNo')
    # listingHashtags = listingObj.get('listingHashtags')
    listingApproved = listingObj.get('listingApproved')
    listingSold = listingObj.get('listingSold')

    # property name is being transmitted, we need to check if it is from an existing property or new
    # if its a new name typed in and already in database return Name already in datababase and return
    # if the name is already in the database but is from the same id it updates the property
    check_name_query = execute_query("SELECT property_id FROM properties WHERE name = %s", listingName)
    if check_name_query:
        if not int(propId) == check_name_query[0][0]:
            print("Property already exists")
            return 'Property already exists'

    # check if the property to update exists, if yes proceeds with updating the database
    print("Changing data from property with id = ", propId)
    query = "SELECT * FROM properties WHERE property_id = %s"
    listingRows = execute_query(query, propId)
    print("Property to update is = ", listingRows)

    if len(listingRows) > 0:
        propertyId = listingRows[0][0]
        print(type(propertyId))

        query = "UPDATE properties SET name = %s, " \
                "price = %s, square_meter = %s, " \
                "rooms = %s, city = %s, zipcode = %s, " \
                "street = %s, street_nr = %s, " \
                "approved = %s, sold = %s  " \
                "WHERE property_id = %s"

        execute_query(query, listingName, listingPrice, listingSqm,
                         listingRooms, listingCity, listingZip, listingStreet,
                         listingStreetNo, listingApproved, listingSold, propertyId)

        print('Updated text information of property in db')
        return 'Updated text information of property in db'
    else:
        print('Property to update was not found')
        return 'Property to update was not found'

############################################# PUT ##################################################
''' --- Updates the DB entry of a property from 0 to 1, if a business manager approves it.  --- '''
####################################################################################################
@application.route('/approve-listing', methods=['POST'])
def approve_listing():
    approveObj = request.get_json()
    id = approveObj.get('id')
    check = 1
    print("Methode print listing")
    query = "UPDATE properties SET approved = %s " \
            "WHERE property_id = %s"
    print (query)
    result = execute_query(query, check, id)
    return jsonify(result)

###################################### GET, PUT, POST ##############################################
''' --- Image Upload Endpoint: 'upload_image' updates the photo path of a certain
        listing in the DB. It calls different helper functions to verify format and size 
        of the file. --- '''

# @author Oliver Kovarna and David Witek
####################################################################################################
@application.route('/image-upload', methods=['GET', 'PUT', 'POST'])
def upload_image():
    header_dict = dict(request.headers)
    listing_name = header_dict.get('Listingname')
    file_size = header_dict.get('Filesize')
    id = header_dict.get('Id')

    if request.method == 'PUT' or request.method =='POST':
        if request.files:
            if not allowed_image_filesize(file_size):
                return 'File exceeded maximum size'

            image = request.files['image']

            if image.filename == '':
                return 'Image must have a filename'

            if not allowed_image(image.filename):
                return 'That image extension is not allowed'

            else:
                filename = secure_filename(image.filename)
                image.save(os.path.join('./static/images/properties/', filename))

                if id:
                    property_id = id
                else:
                    query = "SELECT property_id FROM properties WHERE name = %s"
                    listing_rows = execute_query(query, listing_name)

                    if len(listing_rows) > 0:
                        property_id = listing_rows[0][0]
                    else:
                        return 'No property with specified ID in db'

                query = "UPDATE properties SET photo_path = %s WHERE property_id = %s"
                execute_query(query, os.path.join('./static/images/properties/', filename), property_id)

            return 'Image saved'

    if request.method == 'GET':
        return render_template('Main/Listings/ManageListing.html')

############################################ POST ##################################################
''' --- Enters a new entry into the DB if customer clicked on "Marked as interesting". New DB entry
        will look like this:    Primary Key (auto increment integer), Customer ID, property ID 
        Guarantees that there won't be 2 identical rows. --- '''
####################################################################################################
###################################### Created by Elisabeth and Darya ##############################
@application.route('/markPropAsInteresting', methods=['POST'])
def markPropAsInteresting():
    listingObj = request.get_json()
    userID = listingObj.get('userID')
    propID = listingObj.get('propID')

    # first check if customer already marked current property as interesting
    query = "SELECT * FROM interests WHERE ParticipantID = %s and property_ID = %s "
    alreadyMarked = execute_query(query, userID, propID)

    if len(alreadyMarked) > 0:
        # Fehlermeldung: existiert schon
        print("Customer already marked property as interesting")
    else:

        query = "INSERT INTO interests (ParticipantID, property_ID)" \
                " VALUES(%s, %s)"

        execute_query(query, userID, propID)

        print('Inserted new property into: marked as interesting table')
        return redirect(request.url)

############################################# GET ##################################################
''' --- Returns all properties that a customer with a specific ID marked as interesting.  --- '''
####################################################################################################
# TODO use JOIN instead of two selects and a for-loop
@application.route('/get-marked-properties/<userID>', methods=['GET'])
def getMarkedProperties(userID):
    print("User ID is = ", userID)

    # get all marked properties
    query = "SELECT * FROM interests WHERE ParticipantID = %s"
    # query = "SELECT * FROM interests"
    markedListings = execute_query(query, userID)
    print(markedListings)
    all_marked_listings = []

    for i in range(len(markedListings)):
        query2 = "SELECT * FROM properties WHERE property_id = %s AND is_deleted != 1 AND sold = 0"
        next_listing = execute_query(query2, markedListings[i][2])
        if not next_listing:
            print("No properties marked as interesting")
            continue
        else:
            print("next listing: ", next_listing)
            all_marked_listings.append(next_listing[0])
            print("all listings: ", all_marked_listings)
    all_marked_listings = tuple(all_marked_listings)

    if len(markedListings) <= 0:
        # Fehlermeldung: existiert schon
        print("No properties marked as interesting")
        return jsonify(all_marked_listings)
    else:
        print('Got listings that are marked as interesting')
        return jsonify(all_marked_listings)

############################################ POST ##################################################
''' --- Creates a DB entry for a new property. Guarantees that there won't be two properties with an
        identical name. --- '''
###################################### Created by Joshua,Elisabeth, Darya and David ################
@application.route('/createlisting/user/id/<userID>', methods=['POST'])
def createlisting(userID):
    Agent_id = userID
    '''dataObj = request.get_json()
    listingName = dataObj.get('listing_name')
    print(listingName)
    query = "INSERT INTO test_db.properties (name) VALUES (%s)"
    result = execute_query(query, listingName)
    # fetch result in order to retrieve data'''
    listingObj = request.get_json()
    listingName = listingObj.get('listingName')
    listingPrice = listingObj.get('listingPrice')
    listingSqm = listingObj.get('listingSqm')
    listingRooms = listingObj.get('listingRooms')
    listingZip = listingObj.get('listingZip')
    listingCity = listingObj.get('listingCity')
    listingStreet = listingObj.get('listingStreet')
    listingStreetNo = listingObj.get('listingStreetNo')
    # listingHashtags = listingObj.get('listingHashtags')
    listingApproved = 0

    # TODO einfach immer einfuegen?!
    # query = "SELECT property_id FROM properties WHERE name = %s and is_deleted = 0"

    query = "SELECT property_id FROM properties WHERE name = %s"
    listingRows = execute_query(query, listingName)

    if len(listingRows) > 0:
        # Fehlermeldung: existiert schon
        print("Property already exists")
        return 'Property already exists'
    else:
        query = "INSERT INTO test_db.properties (name, price, square_meter, rooms, city, zipcode, street, street_nr, approved, agent_id_fk, is_deleted)" \
                " VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        execute_query(query, listingName, listingPrice, listingSqm,
                      listingRooms, listingCity, listingZip, listingStreet,
                      listingStreetNo, listingApproved, Agent_id, 0)

        result = execute_query("SELECT property_id FROM properties WHERE name = %s", listingName)
        property_id = result[0][0]
        print("newly created propertyId: ", property_id)
        print('Inserted new property with id' + str(property_id) + ' into DB')
        return jsonify(property_id)

############################################ GET ###################################################
''' --- Renders the about page of the specified team member. --- '''

# @author Oliver Kovarna
####################################################################################################
@application.route('/user/id/<userId>/about/<name>', methods=['GET'])
def render_about_page(userId, name):
    if name == 'Oliver':
        return render_template('About/Oliver Kovarna/index.html')
    elif name == 'Joshua':
        return render_template('About/Joshua Rahimi/index.html')
    elif name == 'Elisabeth':
        return render_template('About/Elisabeth Milde/index.html')
    elif name == 'Darya':
        return render_template('About/Darya Traxel/index.html')
    elif name == 'David':
        return render_template('About/David Witek/index.html')

#--------------------------------------------------------------------------------------------------#
#------------------------------------------ SOCKET ------------------------------------------------#
#--------------------------------------------------------------------------------------------------#
#--------------------------------- @author Oliver Kovarna -----------------------------------------#
#--------------------------------------------------------------------------------------------------#

######################################## connect ###################################################
''' --- Socket listener 'connect': The socket server establishes the connection between clients
        and itself --- '''

# @author Oliver Kovarna
####################################################################################################
@socket_.on('connect', namespace='/')
def establish_connection():
    print('Event Handler: establish_connection')
    print('socket connection established...')

################################### confirm connection #############################################
''' --- Socket listener 'confirm connection': Its callback simply prints the sent message from
        the client side to verify that the connection of the client was successful. --- '''

# @author Oliver Kovarna
####################################################################################################
@socket_.on('confirm connection')
def handle_connection_confirmation(message):
    print('Event Handler: handle_connection_confirmation')
    print(message)

################################### refresh partner chat ###########################################
''' --- Socket listener 'refresh partner chat': Its callback takes a message, the userId and
        the name of the chat partner the user is sending the message to. After fetching the
        name of the requesting user and the id of the chat partner the socket server emits 
        an event 'refreshed partner chat' to refresh the chat on the partner's client side. 
        It updates the name of the chat partner and makes a broadcast to all connected users. 
        However, only the chat of the user with matching userId and chat partner name is 
        refreshed. --- '''

# @author Oliver Kovarna
####################################################################################################
@socket_.on('refresh partner chat')
def handle_partner_chat_refresh(data):
    print('Event Handler: handle_partner_chat_refresh')
    print('received message: ' + data['message'] + ', ' + data['senderUserId'] + ', ' + data['senderChatPartnerName'])

    user_rows = execute_query("SELECT Username FROM participant WHERE ParticipantId='" + data['senderUserId'] + "'")

    user_id_rows = execute_query("SELECT ParticipantId FROM participant WHERE Username='" + data['senderChatPartnerName'] + "'")

    if len(user_rows) > 0:
        sender_name = user_rows[0][0]
        sender_chat_partner_id = user_id_rows[0][0]

        emit('refreshed partner chat', {
            'message': data['message'],
            'senderChatPartnerName': data['senderChatPartnerName'],
            'senderChatPartnerId': str(sender_chat_partner_id),
            'senderName': sender_name,
            'senderUserId': data['senderUserId']
        }, broadcast=True)
    else:
        return 'No username with specified ID could ne found!'

############################### refresh partner main page ##########################################
''' --- Socket listener 'refresh partner main page': Its callback takes a message, the userId and
        the name of the chat partner the user is sending the message to. After fetching the
        name of the requesting user and the id of the chat partner the socket server emits 
        an event 'refreshed partner main page' to refresh the main page of the chat partner 
        to show notifications (new messages). However, only the main page of the user with 
        matching userId and chat partner id is refreshed. --- '''

# @author Oliver Kovarna
####################################################################################################
@socket_.on('refresh partner main page')
def handle_partner_main_page_refresh(data):
    print('Event Handler: handle_partner_main_page_refresh')
    print(
        'received message: ' + data['message'] + ', ' + data['senderUserId'] + ', ' + data['senderChatPartnerName'])

    user_rows = execute_query("SELECT Username FROM participant WHERE ParticipantId='" + data['senderUserId'] + "'")

    user_id_rows = execute_query(
        "SELECT ParticipantId FROM participant WHERE Username='" + data['senderChatPartnerName'] + "'")

    if len(user_rows) > 0:
        sender_name = user_rows[0][0]
        sender_chat_partner_id = user_id_rows[0][0]

        emit('refreshed partner main page', {
            'message': data['message'],
            'senderChatPartnerId': str(sender_chat_partner_id),
            'senderUserId': data['senderUserId']
        }, broadcast=True)
    else:
        return 'No username with specified ID could ne found!'

################################### refresh partner chat activity ##################################
''' --- Socket listener 'refresh partner chat activity': Its callback takes a message, the userId and
        the name of the chat partner the user is sending the message to. After fetching the
        name of the requesting user and the id of the chat partner the socket server emits 
        an event 'refreshed partner chat activity' to refresh the partner's activity in the 
        specific user chat. --- '''

# @author Oliver Kovarna
####################################################################################################
@socket_.on('refresh partner chat activity')
def handle_partner_chat_activity_refresh(data):
    print('Event Handler: handle_partner_chat_activity_refresh')
    print('received message: ' + data['message'] + ', ' + data['senderUserId'] + ', ' + data['senderChatPartnerName'])

    user_rows = execute_query("SELECT Username FROM participant WHERE ParticipantId='" + data['senderUserId'] + "'")

    user_id_rows = execute_query("SELECT ParticipantId FROM participant WHERE Username='" + data['senderChatPartnerName'] + "'")

    if len(user_rows) > 0:
        sender_name = user_rows[0][0]
        sender_chat_partner_id = user_id_rows[0][0]

        emit('refreshed partner chat activity', {
            'message': data['message'],
            'content': data['content'],
            'senderChatPartnerName': data['senderChatPartnerName'],
            'senderChatPartnerId': str(sender_chat_partner_id),
            'senderName': sender_name,
            'senderUserId': data['senderUserId']
        }, broadcast=True)
    else:
        return 'No username with specified ID could ne found!'


####################################################################################################
''' Function uses given SQL string and a variable amount of values to create a SQL query and ensures
    that there is no SQL Injection through cur.execute()'''
# @Author David Witek
####################################################################################################
def execute_query(query, *args):
    cur = mysql.connection.cursor()
    cur.execute('SET NAMES utf8mb4')
    if args:
        cur.execute(query, args)
    else:
        cur.execute(query)
    result = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return result

###################################### HELPER FUNCTION #############################################
''' --- Helper function: 'allowed_image' checks if a file has a valid file format 
                         (PNG, JPG, JPEG). --- '''
# @author Oliver Kovarna
####################################################################################################
def allowed_image(filename):
    if not '.' in filename:
        return False
    ext = filename.rsplit('.', 1)[1]
    if ext.upper() in ['PNG', 'JPG', 'JPEG']:
        return True
    else:
        return False

###################################### HELPER FUNCTION #############################################
''' --- Helper function: 'allowed_image_filesize' checks if a file has a valid file size 
                         (approximately 0.02 GiB). --- '''
# @author Oliver Kovarna
####################################################################################################
def allowed_image_filesize(filesize):
    if int(filesize) <= 0.02 * 1024 * 1024 * 1024:
        return True
    else:
        return False


if __name__ == "__main__":
    socket_.run(app=application, debug=True)



