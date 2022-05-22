var myLogin = angular.module("myLogin", []);

myLogin.controller("registerController", ($scope, $http) => {
    /*
     * This controller function is for registering a new user for the application.
     */
    $scope.sendRegisterData = function() {
        let userName = $scope.usernameModel;
        let email = $scope.emailModel;
        let password1 = $scope.passwordModel1;
        let password2 = $scope.passwordModel2;
        let register_as_agent = document.getElementById("register_as_agent").checked;

        let emailRegEx = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        let emailTest = String(email).toLowerCase();

        if (password1 === password2 && emailRegEx.test(emailTest)) {
            let dataObj = {
                userName,
                email: emailTest,
                password: password1,
                register_as_agent: register_as_agent
            };
            $http.post('/registration', dataObj)
            .then((response) => {
                console.log('Post request has passed!');
                console.log('response data is:', response.data);
                $scope.usernameModel = '';
                $scope.emailModel = '';
                $scope.passwordModel1 = '';
                $scope.passwordModel2 = '';
            }).catch((err) => {
                console.log('Post request has failed!');
                console.log(err);
            });
        } else {
            alert('Please check your password inputs for equality and make sure your email address is in valid format!');
        }
    }
});


myLogin.controller("loginController", ($scope, $http) => {
    /*
     * This controller function is for logging the user in.
     */
    $scope.sendLoginData = function() {
        let userName = $scope.usernameModel;
        let password = $scope.passwordModel;
        let dataObj = {
            userName,
            password,
        };
        $http.post('/login', dataObj)
        .then((response) => {
            let userId = response.data;
            window.sessionStorage.setItem('userId', userId);
            console.log('Seesion UserId', window.sessionStorage.getItem('userId'));
            console.log('Post request has passed!');
            if (Number.isInteger(parseInt(userId))) {
                window.location.href = '/user/id/' + userId;
            } else {
                alert(response.data);
            }
        }).catch((err) => {
            console.log(err);
        });
    }
});
