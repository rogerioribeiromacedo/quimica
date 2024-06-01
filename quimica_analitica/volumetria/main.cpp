#include <QtWidgets>
#include "mainwidget.h"

int main(int argc, char *argv[]) 
{
    // Create an intance of QApplication
    QApplication application(argc, argv);
    application.setStyleSheet("styles.qss");

    // MainWidget class container
    MainWidget w;
    w.showMaximized();
    w.show();

    // Run the application
    return application.exec();
}