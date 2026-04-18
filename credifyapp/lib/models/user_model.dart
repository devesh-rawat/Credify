class UserCreate {
  final String email;
  final String password;
  final String fullName;

  UserCreate({
    required this.email,
    required this.password,
    required this.fullName,
  });

  Map<String, dynamic> toJson() => {
        'email': email,
        'password': password,
        'full_name': fullName,
      };
}

class UserLogin {
  final String email;
  final String password;

  UserLogin({
    required this.email,
    required this.password,
  });

  Map<String, dynamic> toJson() => {
        'email': email,
        'password': password,
      };
}

class Token {
  final String accessToken;
  final String tokenType;
  final String? userId;
  final String? role;
  final String? fullName;

  Token({
    required this.accessToken,
    required this.tokenType,
    this.userId,
    this.role,
    this.fullName,
  });

  factory Token.fromJson(Map<String, dynamic> json) {
    return Token(
      accessToken: json['access_token'] as String,
      tokenType: json['token_type'] as String,
      userId: json['user_id'] as String?,
      role: json['role'] as String?,
      fullName: json['full_name'] as String?,
    );
  }

  Map<String, dynamic> toJson() => {
        'access_token': accessToken,
        'token_type': tokenType,
        if (userId != null) 'user_id': userId,
        if (role != null) 'role': role,
        if (fullName != null) 'full_name': fullName,
      };
}
