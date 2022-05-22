from flask import Blueprint, render_template, redirect


# create the subcomponent to register in blueprint.py
# @author David Witek
blueprint = Blueprint('test_blueprint', __name__, template_folder='templates')



##################################### Route to login page ###########################################
''' --- Sets the route to the first page which ALL users will see (customers, agents and BMs) --- '''
#####################################################################################################
@blueprint.route('/', methods=['GET'])
def render_home():
     return render_template('login.html')



###################################### Route to main page ###########################################
''' --- Sets the route to the main page if user clicks on back button on About page. 
        Main pages look differently according to the user's role --- '''
# @author David Witek
#####################################################################################################
@blueprint.route('/user/id/<userId>/back-to-mainpage', methods=['GET'])
def get_back_to_mainpage_user(userId):
    return redirect('/user/id/' + userId)



###################################### Route to about page ###########################################
''' --- Sets the route to the about page.  --- '''
######################################################################################################
@blueprint.route('/about/<userId>', methods=['GET'])
def render_about(userId):
    return render_template('About/A_main/about_main_new.html')



###################################### Route to HouseMatch start ###########################################
###################################### Created by Joshua and Elisabeth###########################################
@blueprint.route('/user/id/<userId>/hm-start', methods=['GET'])
def render_hm_start(userId):
    return render_template('Housematch/hm_start.html')


###################################### Route to HouseMatch Results ###########################################
###################################### Created by Joshua and Elisabeth###########################################
@blueprint.route('/user/id/<userId>/hm-results', methods=['GET'])
def render_hm_results(userId):
    return render_template('Housematch/hm_results.html')


###################################### Route to HouseMatch  main Site###########################################
###################################### Created by Joshua and Elisabeth###########################################
@blueprint.route('/user/id/<userId>/hm-main', methods=['GET'])
def render_hm_main(userId):
    return render_template('Housematch/hm_main.html')



###################################### Route to edit page ###########################################
''' --- Sets the route to the edit page of a certain property. Agents can edit every single DB entry 
        of their own properties. --- '''
#####################################################################################################
@blueprint.route('/user/id/<userId>/listing/update', methods=['GET'])
def render_listing_update(userId):
    return render_template('Main/Listings/ManageListing.html')



###################################### Route to edit page ###########################################
''' --- Sets the route to the edit page of a certain property. Agents can edit every single DB entry 
        of their own properties. --- '''
#####################################################################################################
@blueprint.route('/user/id/<userId>/main-agent/managelisting/<propId>', methods=['GET'])
def render_malisting(userId, propId):
    return render_template('Main/Listings/ManageListing.html')



################################## Route to interesting page ########################################
''' --- Sets the route to the page, where customer's can see, which properties they marked as 
        interesting. --- '''
#####################################################################################################
@blueprint.route('/user/id/<userId>/profile/interests', methods=['GET'])
def render_interests(userId):
    return render_template('Main/Interest.html')



###################################### Route to help page ###########################################
''' --- Sets the route to the help page.  --- '''
#####################################################################################################
@blueprint.route('/help', methods=['GET'])
def render_help():
    return render_template('Main/get_help.html')



################################## Route to switched view page ######################################
''' --- Sets the route to the switched view. Agent's can switch to view the page as a customer -- '''
#####################################################################################################
@blueprint.route('/SwitchView', methods=['GET'])
def render_view():
    return render_template('Main/main_customer.html')



#################################### Route to edit user page ########################################
''' --- Sets the route to the edit user page. BMs can change passwords of users. --- '''
#####################################################################################################
###################################### Created by Darya##############################################
@blueprint.route('/user/id/<userId>/manageUsers', methods=['GET'])
def render_manageUsers(userId):
    return render_template('Main/manage_Participants_BManager.html')



############################### Route to manage customers page ######################################
''' --- Sets the route to the manage customers page. --- '''
#####################################################################################################
###################################### Created by Darya##############################################
@blueprint.route('/user/id/<userId>/manageCustomers', methods=['GET'])
def render_manageCustomers(userId):
    return render_template('Main/manage_Participants_Agent.html')



#################################### Route to add property page ######################################
''' --- Sets the route to the add property page. Only agents can upload new properties. After that, 
        BMs will have to approve the new property. Only approved properties are shown to customers.
        --- '''
#####################################################################################################
@blueprint.route('/user/id/<userId>/addListings', methods=['GET'])
def render_addListing(userId):
    return render_template('Main/Listings/CreateListing.html')



################################# Route to approve property page ####################################
''' --- Sets the route to the approve property page. After a new property is added, a BM has to 
        approve it before it can be shown to customers. --- '''
#####################################################################################################
@blueprint.route('/user/id/<userId>/approveListing/<propId>', methods=['GET'])
def render_apprlisting(userId, propId):
    return render_template('Main/Listings/ApproveListing.html')




###################################### Route to detail page ###########################################
''' --- Sets the route to the detail page of a certain property. If a user is interested in a 
        property, he or she can get more detailed information by clicking on it. --- '''
#######################################################################################################
@blueprint.route('/user/id/<userId>/ViewPropertyDetails/<propId>', methods=['GET'])
def render_details(userId, propId):
    print('property Id is:', propId)
    return render_template('Main/Listings/PropertyDetails.html')

###################################### Created by Darya##############################################
@blueprint.route('/user/id/<userId>/OnlyViewPropertyDetails/<propId>', methods=['GET'])
def render_details_agent_manager(userId, propId):
    print('property Id is:' + propId)
    return render_template('Main/Listings/Agent_ManagerPropertyDetails.html')



################################## Route to edit profile page #######################################
''' --- Sets the route to the edit profile page of a certain user. Every user can change their first
        and last name. Only BMs can change passwords. --- '''
#####################################################################################################
@blueprint.route('/edit_profile/<userId>', methods=['GET'])
def render_edit_profile(userId):
    return render_template('Main/Edit_Profile.html')

###################################### Created by Darya##############################################
@blueprint.route('/editProfileAgentBM/<userId>', methods=['GET'])
def render_edit_profileAgent(userId):
    return render_template('Main/Edit_Profile_Agent_BM.html')



##################################### Route to profile page #########################################
''' --- Sets the route to the profile page of a certain user. --- '''
#####################################################################################################
@blueprint.route('/user/id/<userId>/profile', methods=['GET'])
def render_own_profile(userId):
    return render_template('Main/Profile.html')



############################# Route to user's profile page as agent #################################
''' --- Sets the route to the profile page of a certain user. Not the user himself is viewing his
        profile but an agent. --- '''
#####################################################################################################
###################################### Created by Darya##############################################
@blueprint.route('/user/id/<userId>/profileAgentBM', methods=['GET'])
def render_profile_agent(userId):
    return render_template('Main/Profile_as_Agent_BM.html')
