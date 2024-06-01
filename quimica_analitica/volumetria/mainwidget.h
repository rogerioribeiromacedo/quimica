#ifndef MAINWIDGET_H
#define MAINWIDGET_H

#include <QWidget>

// Declaration of MainWidget class
class MainWidget : public QWidget 
{
    Q_OBJECT

public:
    explicit MainWidget(QWidget *parent = 0); // Creator
    ~MainWidget(); // Destructor
};

#endif // MAINWIDGET_H