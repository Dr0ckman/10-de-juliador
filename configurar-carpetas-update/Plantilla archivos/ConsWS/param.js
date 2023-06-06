var url = 'ws://[IP]:8181';
var TOwin = 20; // timeout [seg] ventanas 
var TOenc = 10; // timeout [seg] encuesta
var ConfirmaID = 'N'; // R(ut) / F(ono) / N(o) / Auto
var MotCierre = 'S'; // S(i) / N(o)
var IdPausaFin = 3; // Pausa luego del Cierre de Atencion
var RutManMin = 4; // RUT: Mantisa minima
var RutExcs = '1-9,2-7'; // RUT: excepciones
var OfertaTipo = ''; // 'P' = popup, 'C' = Caja Contenido, 'PC' = Ambos, '' = No habilitada
var Qrellamado = 1;

// Parametros de Encuesta Web
var EncWOK = false; // Booleano
var EncWTipo = 'DESPUES'; //DESPUES / DURANTE
var EncWTMin = 10; // [seg] minimo para habilitar Enc en atencion