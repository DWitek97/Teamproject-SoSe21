var main_customer = angular.module("main_customer",  []);

main_customer.controller("main_customerController", ($scope, $http) => {
    /*  SOCKET Client  */
    $scope.connectionOptions =  {
        "force new connection" : true,
        "reconnectionAttempts": "Infinity",
        "timeout" : 10000,
        secure: true
    };
    // initialize socket client and send a connect request to the socket server.
    $scope.socket = io.connect('https://' + document.domain + '/', $scope.connectionOptions);

    /*
     * The callback in the listener 'connect' is used to connect the client with the socket.
     * It emits an event on the socket server side and sends a certain message as well as the userId
     * to confirm its successful connection.
     *
     * @author Oliver Kovarna
     */
    $scope.socket.on('connect', function() {
        $scope.socket.emit('confirm connection', {
            message: 'client is connected to the SocketServer...',
            userId: window.sessionStorage.getItem('userId')
        });
    });

    /*
     * The callback in the listener 'refreshed partner main page' updates the main page of a chat partner
     * when he receives new messages (new notifications).
     *
     * @author Oliver Kovarna
     */
    $scope.socket.on('refreshed partner main page', function(data) {
        let userId = window.sessionStorage.getItem('userId');

        if(data.senderUserId !== userId && data.senderChatPartnerId === userId) {
            $scope.getNotifications();
        }
    });

    $scope.isNotificationCountVisible = false;
    $scope.notificationNumber = '';

    /*
     * The controller function 'getNotifications' retrieves all chat notifications for a certain user and displays
     * them on its main page. The notifications appear as a red circle with the current number of new messages on the
     * speech bubble.
     *
     * @author Oliver Kovarna
     */
    $scope.getNotifications = function() {
        let userId = window.sessionStorage.getItem('userId');

        $http.get('/user/id/' + userId + '/chat/notifications')
        .then((response) => {
            $scope.notifications = response.data.notificationCount;
            $scope.notificationButton = angular.element(document.getElementById('notification_btn'))[0];

            if ($scope.notifications > 0) {
                $scope.isNotificationCountVisible = true;
                $scope.notificationNumber = $scope.notifications;

                if ($scope.notificationButton.classList.length < 1) {
                    $scope.notificationButton.classList.add('notification');
                }
            }
            else {
                $scope.isNotificationCountVisible = false;
                $scope.notificationNumber = '';

                if ($scope.notificationButton.classList.length > 0) {
                    $scope.notificationButton.classList.remove('notification');
                }
            }
        }).catch((err) => {
            console.log(err);
        });
    }

    $scope.getNotifications();

    let userId = window.sessionStorage.getItem('userId');
    $scope.properties = [];
    $scope.single_property = [];
    $scope.yeet = [];
    $scope.content = [];
    $scope.profiles;
    $scope.propertyID = 0;
    $scope.markedProperties = [];
    $scope.unapprovedListings = [];
    $scope.new_prop_id; // will hold the id of the newly added property
    $scope.memberName1 = 'Joshua'
    $scope.memberName2 = 'Darya'
    $scope.memberName3 = 'David'
    $scope.memberName4 = 'Oliver'
    $scope.memberName5 = 'Elisabeth'

    $scope.getAboutPage = function(name) {
        let userId = window.sessionStorage.getItem('userId')
        let memberName = name;

        $http.get('/user/id/' + userId + '/about/' + memberName)
        .then((response) => {
            window.location.href = '/user/id/' + userId + '/about/' + memberName;
        }).catch((err) => {
            console.log(err);
        });
    }


    $scope.getMainAboutPage = function() {
        $http.get('/about/' + userId)
        .then((response) => {
            window.location.href = '/about/' + userId;
        }).catch((err) => {
            console.log(err);
        });
    }


 // --------------------------------------------- HOUSEMATCH --------------------------------------------------------
    // Created by Joshua and Elisabeth
    $scope.checkedHTs;
    $scope.matching_props;
    $scope.match_pcs;

    $scope.getHMStart = function() {
        let userId = window.sessionStorage.getItem('userId');
        $http.get('/user/id/' +  userId + '/hm-start')
        .then((response) => {
            window.location.href = '/user/id/' +  userId + '/hm-start';
        }).catch((err) => {
            console.log(err);
        });
    }
    //Created by Joshua
        $scope.get_all_hashtags = function() {
        console.log("init()");
        $http.get('/get-all-hashtags')
        .then((response) => {
        console.log(response.data)
            $scope.hashtags = response.data;
            $scope.allHashtags = $scope.hashtags;
            console.log("Wir sind in der Hashtagfunktion");
        }).catch((err) => {
            console.log(err)
        });
        return $scope.hashtags;
    }



    $scope.getHMResult = function() {
        let userId = window.sessionStorage.getItem('userId');
        $http.get('/user/id/' +  userId + '/hm-results')
        .then((response) => {
            window.location.href = '/user/id/' +  userId + '/hm-results';
        }).catch((err) => {
            console.log(err);
        });
    }

    $scope.initHMResults = function() {
        let results = window.sessionStorage.getItem('HMresults');
        console.log("Session storage is = ", window.sessionStorage.getItem('HMresults'));
        let userId = window.sessionStorage.getItem('userId')
        let res_arr = results.split(",");
        //let json_res = JSON.parse(results);
        //console.log("Json result = ", json_res);
        let res_ids = []
        let res_pcs = []

        console.log("Result is = ", res_arr);

        /*for (var i = 0; i < res_arr.length-1; i=i+2) {
            res_ids[i/2] = res_arr[i];              // holds the ids
            res_pcs[i/2] = res_arr[i+1];            // holds the percentage of the match
        }*/

        for (var i = 0; i <= res_arr.length-1; i++) {
            if(i % 2 == 0) {
                res_ids.push(res_arr[i])
            } else {
                res_pcs.push(res_arr[i])
            }
        }

        console.log("Result ids = ", res_ids);
        console.log("Result pcs = ", res_pcs);
        $scope.match_pcs = res_pcs;

        var dataObj = {
            prop_ids: res_ids
        }

        $scope.matching_props = [];
        $scope.prop_and_perc = [];

        $http.post('/user/id/' +  userId + '/hm-result-properties', dataObj)
        .then((response) => {
            if (response.data =="No Properties found") {
                document.getElementById("nomatching").innerHTML = "No matching properties found. Please try again."
            }else{
                console.log("properties are = ", response.data);
                $scope.matching_props = response.data;
            }
        }).catch((err) => {
            console.log(err);
        });

        //console.log("properties are = ", $scope.matching_props);

    }

    $scope.getHMMain = function() {
        let userId = window.sessionStorage.getItem('userId');
        $http.get('/user/id/' +  userId + '/hm-main')
        .then((response) => {
            window.location.href = '/user/id/' +  userId + '/hm-main';
        }).catch((err) => {
            console.log(err);
        });
    }

    $scope.getCheckedMusts = function() {
        let userId = window.sessionStorage.getItem('userId');
        // get all checkboxes that user checked
        let hashtags = $scope.hashtags;
        $scope.checkedHTs = [];
        for(var i = 0; i < hashtags.length; i++) {
            if(hashtags[i].isChecked == true) {
                console.log(hashtags[i]);
                $scope.checkedHTs.push(hashtags[i]);
            }
        }
        console.log("checked hts = ", $scope.checkedHTs);

        var dataObj = {
            hts: $scope.checkedHTs,
            len: $scope.checkedHTs.length
        }
        // send data to backend
        var results = []

        $http.post('/user/id/' +  userId + '/hm-result', dataObj)
        .then((response) => {
            console.log("Response =", response.data);
            //console.log("arr = ", result_ids);
            window.sessionStorage.setItem('HMresults', response.data)
            console.log("Session storage is = ", window.sessionStorage.getItem('HMresults'));
        }).catch((err) => {
            console.log(err);
        });
    }

    /* While CREATING a new listing: the agent choses some hashtags that fit for the property. Those will be stored in
    * the array '$scope.smallItemList */
    $scope.itemList=[];             // holds EVERY hashtag-list ever chosen
    $scope.smallItemList=[];        // holds the last hashtag-list (the one that is final)

    /* Event Listener for the hashtag dropdown menu */
    $scope.changedValue=function(item) {
        $scope.itemList.push(item);
        console.log($scope.itemList);
        $scope.smallItemList = $scope.itemList[$scope.itemList.length-1];
        console.log($scope.smallItemList);
        for (var i = 0; i < $scope.smallItemList.length; i++){
            $scope.smallItemList[i] = parseInt($scope.smallItemList[i].split(":")[0]);
        }
        console.log($scope.smallItemList);
    }

    /* link new HTs to property and store them in DB if user selected HTs in dropdown menu
    *  else: DB will stay the same */
    $scope.updateListingHTs = function(propId) {
        //check if user selected new HTs in dropdown menu
        if($scope.smallItemList.length > 0) {
            //console.log("Update HTs");
            dataObj = {
                propId: propId,
                hts: $scope.smallItemList
            }
            userId = window.sessionStorage.getItem("userId");
            // link new HTs to property and store them in DB
            $http.post('/user/id/' +  userId + '/new-property-hashtags', dataObj)
            .then((response) => {
                console.log("Linked new Hashtags");
            }).catch((err) => {
                console.log(err);
            });
        }
        // do nothing if no HTs are selected
        else {
            console.log("Leave HTs as they are");
        }
    }

    // get hashtags from DB linked to certain property
    $scope.getPropHashtags = function(propId) {
        //console.log("Prop Id in prop hashtags = ", propId);
        dataObj = {
            propId: propId
        }

        $http.post('/user/id/' +  userId + '/property-hashtags', dataObj)
        .then((response) => {
            //console.log("Linked Hashtags =", response.data);
            $scope.linkedHTs = [];          // variable used in ng-repeat to display for user
            for(var i = 0; i < response.data.length; i++) {
                $scope.linkedHTs.push(response.data[i].toString());
            }
        }).catch((err) => {
            console.log(err);
        });
    }
    // ------------------------------ END HOUSEMATCH -------------------------------------------------------------------

   // @author David Witek
    $scope.goBackToMainpage = function() {
        let userId = window.sessionStorage.getItem('userId');
        $http.get('/user/id/' + userId + '/back-to-mainpage')
        .then((response) => {
            window.location.href = '/user/id/' + userId + '/back-to-mainpage';
        }).catch((err) => {
            console.log(err);
        });
    }

    $scope.getViewPropertyDetails = function(id) {
        let userId = window.sessionStorage.getItem('userId');
        $scope.propertyID = id;
        $http.get('/user/id/' +  userId + '/ViewPropertyDetails/' + id)
        .then((response) => {
            window.location.href = '/user/id/' +  userId + '/ViewPropertyDetails/' + id;
        }).catch((err) => {
            console.log(err);
        });
    }

    //Created by Darya
    $scope.getViewAgent_ManagerPropertyDetails = function(id) {
        console.log("id =", id);
        let userId = window.sessionStorage.getItem('userId');
        $http.get('/user/id/' +  userId + '/OnlyViewPropertyDetails/' + id)
        .then((response) => {
            window.location.href = '/user/id/' +  userId + '/OnlyViewPropertyDetails/' + id;
        }).catch((err) => {
            console.log(err);
        });
    }
    //Created by Joshua (needed for randomPassword Change)
    $scope.changePassword = function(id) {
        let listingObj = {
            userid: id
        }
        console.log(listingObj)
        // Listing Text Information Request
        $http.post('/changePassword', listingObj)
        .then((response) => {
            window.location.reload();
        }).catch((err) => {
            console.log(err)
        });
   }

   //Created by Darya
   $scope.changeStatus = function(id) {
        let listingObj = {
             userid: id
        }
        console.log(listingObj)

        $http.put('/changeStatus', listingObj)
        .then((response) => {
            window.location.reload();
            console.log("changed")
        }).catch((err) => {
            console.log(err)
        });
   }

   //Created by Darya
    $scope.changeAccess = function(id) {
        let listingObj = {
             userid: id
        }
        console.log(listingObj)
        $http.put('/changeAccess', listingObj)
        .then((response) => {
            window.location.reload();
            console.log("Access changed")
        }).catch((err) => {
            console.log(err)
        });
   }
    $scope.initProfile = function() {
        console.log("bin in initProfile");
        let userId = window.sessionStorage.getItem('userId');
        console.log(userId)
        // Listing Text Information Request
        $http.get('/getProfile/' +userId)
        .then((response) => {
            $scope.profiles = response.data;
            console.log($scope.profiles);
        }).catch((err) => {
            console.log(err)
        });
       }

    $scope.changeProfile = function() {
        console.log("bin in changeProfile");
        let userId = window.sessionStorage.getItem('userId');
        console.log(userId)
        let profileObj = {
            fname: $scope.fname,
            lname: $scope.lname,
        }
        console.log(profileObj)
        // Listing Text Information Request
        $http.post('/change-profile/' +userId, profileObj)
        .then((response) => {
        }).catch((err) => {
            console.log(err)
        })
        $scope.getProfile();
    };
    // @author David Witek and
    $scope.changeProfileAgent = function() {
        let userId = window.sessionStorage.getItem('userId');
        console.log(userId)
        console.log("scope name", $scope.fname)

        let profileObj = {
            fname: $scope.fname,
            lname: $scope.lname,
            agencyName: $scope.agencyName
        }
        // Listing Text Information Request
        $http.post('/change-profile-agent/' +userId, profileObj)
        .then((response) => {
        }).catch((err) => {
            console.log(err)
        })
        $scope.getProfileAgentBM();
    };

    $scope.getProfile = function() {
        let userId = window.sessionStorage.getItem('userId');
        $http.get('/user/id/' +  userId + '/profile')
        .then((response) => {
            window.location.href = '/user/id/' +  userId + '/profile';
        }).catch((err) => {
            console.log(err);
        });
    }

    //Created by Darya
    $scope.getProfileAgentBM = function() {
        $http.get('/user/id/' +  userId + '/profileAgentBM')
        .then((response) => {
            window.location.href = '/user/id/' +  userId + '/profileAgentBM';
        }).catch((err) => {
            console.log(err);
        });
    }
    //Created by Joshua
    $scope.getAddListings = function() {
        let userId = window.sessionStorage.getItem('userId')
        $http.get('/user/id/' +userId+'/addListings')
        .then((response) => {
            window.location.href = '/user/id/'+userId+'/addListings';
        }).catch((err) => {
            console.log(err);
        });
    }
    //Created by Joshua
    $scope.getManageListing = function() {
        $http.get('/user/id/'+userId+'/manageListing')
        .then((response) => {
            window.location.href = '/user/id/'+userId+'/manageListing';
        }).catch((err) => {
            console.log(err);
        });
    }
    $scope.getManageUsers = function() {
        $http.get('/user/id/'+userId+'/manageUsers')
        .then((response) => {
            window.location.href = '/user/id/'+userId+'/manageUsers';
        }).catch((err) => {
            console.log(err);
        });
    }
      $scope.getManageCustomers = function() {
        $http.get('/user/id/'+userId+'/manageCustomers')
        .then((response) => {
            window.location.href = '/user/id/'+userId+'/manageCustomers';
        }).catch((err) => {
            console.log(err);
        });
    }



    $scope.getManageListingPage = function(propId) {
        $http.get('/user/id/'+userId+'/main-agent/managelisting/' + propId)
        .then((response) => {
            window.location.href = '/user/id/'+userId+'/main-agent/managelisting/' + propId;
        }).catch((err) => {
            console.log(err);
        });
    }
    //Created by Joshua
    $scope.getApproveListing = function(propId) {
        $http.get('/user/id/'+userId+'/approveListing/'+propId)
        .then((response) => {
            window.location.href = '/user/id/'+userId+'/approveListing/'+propId;
        }).catch((err) => {
            console.log(err);
        });
    }

    $scope.initInterests = function() {
        //console.log("In initInterests")
        let userId = window.sessionStorage.getItem('userId');

        let listingObj = {
            userID: userId
        }

        // Make Backend Call to get all properties that are marked as interesting
        $http.get('/get-marked-properties/'+userId)
        .then((response) => {
            $scope.markedProperties = response.data;
        }).catch((err) => {
            console.log(err)
        });
    }

    $scope.getInterestPage = function() {
        let userId = window.sessionStorage.getItem('userId');
        $http.get('/user/id/' +  userId + '/profile/interests')
        .then((response) => {
            window.location.href = '/user/id/' + userId + '/profile/interests';
        }).catch((err) => {
            console.log(err);
        });
    }

    //Created by Elisabeth, Darya
    $scope.markAsInteresting = function() {
        let userId = window.sessionStorage.getItem('userId');
        $scope.initDetails();
        let propId = $scope.propertyID;

        let listingObj = {
            userID: userId,
            propID: propId
        }
        console.log(listingObj)

        // Make Backend Call to update DB
        $http.post('/markPropAsInteresting', listingObj)
        .then((response) => {
        }).catch((err) => {
            console.log(err)
        });
        //show all properties that are marked as interesting including the one just added
        $scope.getInterestPage()
    }

    //Created by Darya
    $scope.getSwitchView = function() {
        $http.get('/SwitchView')
        .then((response) => {
            window.location.href = '/SwitchView';
        }).catch((err) => {
            console.log(err);
        });
    }

    //Created by Darya
    $scope.getHelp = function() {
        $http.get('/help')
        .then((response) => {
            window.location.href = '/help';
        }).catch((err) => {
            console.log(err);
        });
    }

// TODO  combine both functions/endpoints into one ?? //////////////////////////
    $scope.editProfile = function() {
        let userId = window.sessionStorage.getItem('userId');
        $http.get('/edit_profile/' + userId)
        .then((response) => {
            window.location.href = '/edit_profile/' + userId;
        }).catch((err) => {
            console.log(err);
        });
    }

    //Created by Darya
    $scope.editProfileAgentBM = function() {
        let userId = window.sessionStorage.getItem('userId');
        $http.get('/editProfileAgentBM/' + userId)
        .then((response) => {
            window.location.href = '/editProfileAgentBM/' + userId;
        }).catch((err) => {
            console.log(err);
        });
    }

//////////////////////////////////////////////////////////////////////////////

    $scope.getLogout = function() {
        let userId = window.sessionStorage.getItem('userId');
        console.log('userId: ', userId);
        $http.get('/logout?userId=' + userId)
        .then((response) => {
            window.location.href = '/logout?userId=' + userId;
            console.log('userId: ', userId);
        }).catch((err) => {
            console.log(err);
        });
    }

    /*
     * The controller function 'createListing' is for creating a new listing. It makes
     * a request to the backend to add the text information. Another request with the listingName and fileSize
     * as cookies in the header is sent to upload the image.
     */

    //Created by Joshua, Darya, Elisabeth, David
    $scope.createListing = function(reload) {
        let userId = window.sessionStorage.getItem('userId');
        let listingObj = {
            listingName: $scope.listingName,
            listingPrice: $scope.listingPrice,
            listingSqm: $scope.listingSqm,
            listingRooms: $scope.listingRooms,
            listingZip: $scope.listingZip,
            listingCity: $scope.listingCity,
            listingStreet: $scope.listingStreet,
            listingStreetNo: $scope.listingStreetNo,
            listingImage: $scope.listingImage, //Not used in first request, only used for checking if field was filled
        }
        console.log(listingObj);
        // iterate over all fields and check if something was left empty
        for (let prop in listingObj) {
            if (listingObj[prop] == null) {
                alert("Please fill all fields and upload an Image!");
                return;
            }
        }

        if ($scope.smallItemList.length < 1) {
            alert("Please fill all fields and upload an Image!");
            return;
        }

        // Listing Text Information Request
        $http.post('/createlisting/user/id/' +  userId, listingObj)
        .then((response) => {
            if(response.data == "Property already exists") {
                alert("Please chose another name. This property already exists");
                return;
            } else {
                $scope.new_prop_id = response.data;
                window.sessionStorage.setItem("new_prop_id", response.data);
                console.log("new id is = ", $scope.new_prop_id);
                $scope.addHashtagsToDB($scope.new_prop_id);
            }
        }).catch((err) => {
            console.log(err)
        });

         if ($scope.listingImage) {

            let file = $scope.listingImage;
            let fd = new FormData();
            fd.append('image', file);

            // Image Upload Request (cannot be posted as JSON)
            $http.post('/image-upload', fd,  {
                transformRequest: angular.identity,
                headers: {
                    'Content-Type': undefined,
                    'listingName': $scope.listingName,
                    'filesize': $scope.listingImage['size']
                }
            })
            .then((response) => {
                console.log(response.data);
            }).catch((err) => {
                console.log(err);
                alert("An error occurred. Image was NOT uploaded.");
                window.location.reload();
                return;
            });
         }
    }

    $scope.addHashtagsToDB = function(propId) {
        console.log("hashtags are = ", $scope.smallItemList);
        var dataObj = {
            propId: propId,
            hts: $scope.smallItemList
        }

        $http.post('/user/id/' + userId +'/hm-hashtags', dataObj)
            .then((response) => {
                console.log(response.data);
                alert("Successfully uploaded new property!");
            }).catch((err) => {
                console.log(err);
        });
    }

    $scope.getSingleProperty = function(id) {
         $http.get('/get-single-property/' + id)
         .then((response) => {
             $scope.single_property = response.data[0];
             console.log("Single prop = ", $scope.single_property);
         }).catch((err) => {
               console.log(err)
         });
    }

    $scope.approveInit = function() {
        // initialize $scope.propertyID with ID of current property
        $scope.initDetails();
        let id = $scope.propertyID
        // get DB data of current property
        $scope.getSingleProperty(id);
    }

    $scope.get_all_customers = function() {
        $http.get('/get-all-customers')
        .then((response) => {
            $scope.customers = response.data;
        }).catch((err) => {
            console.log(err)
        });
        return $scope.customers;
    }

    $scope.get_all_users = function() {
        $http.get('/get-all-users')
        .then((response) => {
            $scope.users = response.data;
            $scope.allusers = $scope.users;
        }).catch((err) => {
            console.log(err)
        });
        return $scope.users;
    }

    $scope.initDetails = function() {
        let url = window.location.href.split("/");
        console.log("URL: ",url);
        let length = url.length;
        let propId = url[length-1];
        $scope.propertyID = parseInt(propId);
        console.log("Prop Id = ", $scope.propertyID)
        $scope.getSingleProperty($scope.propertyID)
    }

    // @author David Witek and Elisabeth Milde
    $scope.clickSearch = function(is_customer) {
        // check user input in search form
        let userId = window.sessionStorage.getItem('userId');
        let search_term = $scope.keyword;
        console.log("$keyword: ", $scope.keyword);
        console.log("search_term: ", search_term);

        // Agent and manager Filter checkboxes
        sold_checkbox = document.getElementById("Sold").checked;
        my_listing_checkbox = document.getElementById("MyListings").checked;
        pending_checkbox = document.getElementById("Pending").checked;

        let dataObj;

        // apply filters if filter option is on website

        $scope.filterFunction();        //checks which filters the user wants to use and sets values accordingly
        let maxP = $scope.maxPrice;
        console.log("price = ", $scope.maxPrice)
        let maxR = $scope.maxRooms;
        console.log("rooms = ", $scope.maxRooms)
        let maxS = $scope.maxSqm;
        console.log("sqm = ", $scope.maxSqm)

        console.log('sold_checkbox: ', sold_checkbox)
        console.log('my_listing_checkbox: ', my_listing_checkbox)
        console.log('pending_checkbox: ', pending_checkbox)
        console.log('is_customer: ', is_customer)

        // make data array with all user inputs
        dataObj = {
            search_term,
            maxP,
            maxR,
            maxS,
            sold_checkbox,
            my_listing_checkbox,
            pending_checkbox,
            // variable is being given from html as a flag to signal this request is coming from main_customer view
            is_customer
        };

        //send to backend
        $http.post('/user/id/' + userId +'/search', dataObj)
        .then((response) => {
            console.log(response)
            rows = response.data;
            console.log(rows);
            if( !(angular.equals(rows, "No properties found")) && !(angular.equals(rows, "Searchword is too long!"))) {
                $scope.properties = rows;
                document.getElementById("search").innerHTML = "";
            } else {
                document.getElementById("search").innerHTML = rows;
            }
        }).catch((err) => {
            console.log(err)
        });
    }

    $scope.filterFunction = function() {
        // check if user wants to use price filter --> if not: default value for price is 0
        let priceIsChecked = document.getElementById("priceCB").checked;
        if(!priceIsChecked) {
            $scope.maxPrice = 0;
        } else {
            $scope.maxPrice = parseInt(document.getElementById("priceSlider").value);
        }

        // check if user wants to use rooms filter --> if not: default value for rooms is 0
        let roomIsChecked = document.getElementById("roomCB").checked;
        if(!roomIsChecked) {
            $scope.maxRooms = 0;
        } else {
            $scope.maxRooms = parseInt(document.getElementById("roomSlider").value);
        }

        // check if user wants to use sqm filter --> if not: default value for sqms is 0
        let sqmIsChecked = document.getElementById("sqmCB").checked;
        if(!sqmIsChecked) {
            $scope.maxSqm = 0;
        } else {
            $scope.maxSqm = parseInt(document.getElementById("sqmSlider").value);
        }
    }

    $scope.getChatPage = function() {
        console.log('chatPage request')
        let userId = window.sessionStorage.getItem('userId');
        console.log('/user/id/' + userId + '/chat-gui')
        $http.get('/user/id/' + userId + '/chat-gui')
        .then((response) => {
            console.log('Seesion UserId', window.sessionStorage.getItem('userId'));
            console.log('Get request has passed!');
            if (Number.isInteger(parseInt(userId))) {
                window.location.href = '/user/id/' + userId + '/chat-gui';
            }
        }).catch((err) => {
            console.log(err)
        });
    }
    //Created by Joshua,
    $scope.approveListing = function() {
        let prop_id = $scope.single_property[0];
        dataObj = {
            id: prop_id,
        }
        $http.post('/approve-listing', dataObj)
        .then((response) => {
            console.log(response)
        }).catch((err) => {
            console.log(err)
        });
    }




     $scope.deleteListing = function(propertyId) {
        console.log('propertyId: ', propertyId);
        $http.delete('/listing-removal?propertyId=' + propertyId)
        .then((response) => {
            console.log('success');
            alert('The selected property has been removed!')
            $scope.clickSearch();
        }).catch((err) => {
            console.log(err)
        });
    }


    // changes DB based on user input:
    // if new value is entered in form --> DB value will be updated
    // else --> old DB value will be kept
    // @author David Witek and Elisabeth Milde
    $scope.updateListing = function() {
        $scope.initDetails();
        let id = $scope.propertyID;
        let userId = window.sessionStorage.getItem('userId');
        console.log("id = ", id);
        $scope.getSingleProperty(id);
        let name, price, sqm, rooms, zip, city, street, streetno, hashtags, approved, sold;
        //check if user entered new values, if not, use values already in DB
        // name
        if ($scope.listingName != undefined) {
            name = $scope.listingName;
        } else {
            name = $scope.single_property[1]
        }
        // price
        if ($scope.listingPrice != undefined) {
            price = $scope.listingPrice;
        } else {
            price = $scope.single_property[2]
        }
        //sqm
        if ($scope.listingSqm != undefined) {
            sqm = $scope.listingSqm;
        } else {
            sqm = $scope.single_property[3]
        }
        // number of rooms
        if ($scope.listingRooms != undefined) {
            rooms = $scope.listingRooms;
        } else {
            rooms = $scope.single_property[4]
        }
        // zip code
        if ($scope.listingZip != undefined) {
            zip = $scope.listingZip;
        } else {
            zip = $scope.single_property[6]
        }
        // city
        if ($scope.listingCity != undefined) {
            city = $scope.listingCity;
        } else {
            city = $scope.single_property[5]
        }
        // street
        if ($scope.listingStreet != undefined) {
            street = $scope.listingStreet;
        } else {
            street = $scope.single_property[7]
        }
        // street no
        if ($scope.listingStreetNo != undefined) {
            streetno = $scope.listingStreetNo;
        } else {
            streetno = $scope.single_property[8]
        }

        // hashtags
        $scope.updateListingHTs(id);

        // approve listing
        let approve = document.getElementById("inputMaApprove");
        // check if approve tag is there (for agent there won't be an approve tag)
        if(approve != null) {
            //console.log("Approving listing... ")
            approveIsChecked = document.getElementById("inputMaApprove").checked;
            if(approveIsChecked) {
                approved = 1;
            } else {
                approved = 0;
            }
        } else {
            approved = $scope.single_property[10];
        }

        // sold
        let toBeSold = document.getElementById("inputMaSold");
        // check if sold tag is there (just to be sure)
        if(toBeSold != null) {
            console.log("Marking listing as sold... ")
            approveIsChecked = toBeSold.checked;
            if(approveIsChecked) {
                sold = 1;
            } else {
                sold = 0;
            }
        }

        // data object to be sent to DB
        let listingObj = {
            listingName: name,
            listingPrice: price,
            listingSqm: sqm,
            listingRooms: rooms,
            listingZip: zip,
            listingCity: city,
            listingStreet: street,
            listingStreetNo: streetno,
            listingHashtags: $scope.listingHashtags,
            listingApproved: approved,
            listingSold: sold
        }

        // Listing Text Information Request
        $http.put('/listing-update/'+id, listingObj)
        .then((response) => {
            console.log(response.data);
            if(response.data == "Property already exists") {
                alert("Please chose another name. This property already exists");
                return;
            }
            alert("Successfully changed property");
        }).catch((err) => {
            console.log(err)
            alert("An error occurred. Property was NOT changed.");
            window.location.reload();
            return;
        });

        if ($scope.listingImage) {

            console.log("IMAGE: ", $scope.listingImage);
            console.log("NAME: ", $scope.listingImage['name']);

            let file = $scope.listingImage;
            let fd = new FormData();
            fd.append('image', file);

            // Image Upload Request (cannot be posted as JSON)
            $http.post('/image-upload', fd,  {
                transformRequest: angular.identity,
                headers: {
                    'Content-Type': undefined,
                    'listingName': name,
                    'filesize': $scope.listingImage['size'],
                    'id': id
                }
            })
            .then((response) => {
                console.log(response.data);
            }).catch((err) => {
                console.log(err);
                alert("An error occurred. Image was NOT uploaded.");
                window.location.reload();
                return;
            });
        }
    }
});

main_customer.directive('fileModel', ['$parse', function ($parse) {
    return {
       restrict: 'A',
       link: function(scope, element, attrs) {
          var model = $parse(attrs.fileModel);
          var modelSetter = model.assign;

          element.bind('change', function(){
             scope.$apply(function(){
                modelSetter(scope, element[0].files[0]);
             });
          });
       }
    };
 }]);

main_customer.controller("filter_controller", ($scope) => {
/*--------------------------------------------------------------------------------------------------------------------*/
/*-----------------------------------------------SLIDERS--------------------------------------------------------------*/
    /* Price Slider */
    $scope.slider1 = document.getElementById("priceSlider");
    $scope.output1 = document.getElementById("maxPrice");
    $scope.value1 = parseInt($scope.slider1.value);
    $scope.nice_value1 = $scope.value1.toLocaleString();
    $scope.output1.innerHTML = $scope.nice_value1;

    $scope.slider1.oninput = function () {
        $scope.value1 = parseInt($scope.slider1.value);
        $scope.nice_value1 = $scope.value1.toLocaleString();
        $scope.output1.innerHTML = $scope.nice_value1;
    }

    /* Room Slider */
    $scope.slider2 = document.getElementById("roomSlider");
    $scope.output2 = document.getElementById("maxRooms");
    $scope.value2 = parseInt($scope.slider2.value);
    $scope.nice_value2 = $scope.value2.toLocaleString();
    $scope.output2.innerHTML = $scope.nice_value2;

    $scope.slider2.oninput = function () {
        $scope.value2 = parseInt($scope.slider2.value);
        $scope.nice_value2 = $scope.value2.toLocaleString();
        $scope.output2.innerHTML = $scope.nice_value2;
    }

    /* Sqm Slider */
    $scope.slider3 = document.getElementById("sqmSlider");
    $scope.output3 = document.getElementById("maxSqm");
    $scope.value3 = parseInt($scope.slider3.value);
    $scope.nice_value3 = $scope.value3.toLocaleString();
    $scope.output3.innerHTML = $scope.nice_value3;

    $scope.slider3.oninput = function () {
        $scope.value3 = parseInt($scope.slider3.value);
        $scope.nice_value3 = $scope.value3.toLocaleString();
        $scope.output3.innerHTML = $scope.nice_value3;
    }
/*--------------------------------------------------------------------------------------------------------------------*/
});

