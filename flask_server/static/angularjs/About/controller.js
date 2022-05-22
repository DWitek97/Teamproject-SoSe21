var about = angular.module("about", []);

about.controller("aboutController", ($scope, $http) => {
    $scope.memberName1 = 'Joshua'
    $scope.memberName2 = 'Darya'
    $scope.memberName3 = 'David'
    $scope.memberName4 = 'Oliver'
    $scope.memberName5 = 'Elisabeth'

    $scope.getAboutPage = function(name) {
        let userId = window.sessionStorage.getItem('userId')
        let memberName = name;
        console.log(memberName);

        $http.get('/user/id/' + userId + '/about/' + memberName)
        .then((response) => {
            window.location.href = '/user/id/' + userId + '/about/' + memberName;
        }).catch((err) => {
            console.log(err);
        });
    }

    $scope.goBackToMainpage = function() {
        let userId = window.sessionStorage.getItem('userId');
        $http.get('/user/id/' + userId + '/back_to_mainpage')
        .then((response) => {
            window.location.href = '/user/id/' + userId + '/back_to_mainpage';
        }).catch((err) => {
            console.log(err);
        });
    }

    $scope.getMainAboutPage = function() {
        $http.get('/about')
        .then((response) => {
            window.location.href = '/about';
        }).catch((err) => {
            console.log(err);
        });
    }
});
