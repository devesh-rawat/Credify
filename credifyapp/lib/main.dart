import 'package:credifyapp/routes/app_routes.dart';
import 'package:credifyapp/theme/theme.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'providers/auth_provider.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Create and initialize auth provider before app starts
  final authProvider = AuthProvider();
  await authProvider.initialize();
  
  runApp(MyApp(authProvider: authProvider));
}

class MyApp extends StatelessWidget {
  final AuthProvider authProvider;
  
  const MyApp({super.key, required this.authProvider});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider.value(
      value: authProvider,
      child: MaterialApp(
        title: "Credify App",
        theme: lightTheme,
        darkTheme: darkTheme,
        themeMode: ThemeMode.system,
        routes: AppRoutes.routes,
      ),
    );
  }
}