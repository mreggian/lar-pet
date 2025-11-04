#include "TGeoManager.h"
#include "TGeoTube.h"



void visualize_geometry(){

    gSystem->Load("libGeom");
    gSystem->Load("libGdml");

    TGeoManager *geom = TGeoManager::Import("prototype_geometry.gdml");

    TGeoVolume *vol = geom->GetVolume("volCathodeDisk");
    vol->SetLineColor(kRed);
    vol->SetTransparency(0);

    TGeoVolume *volAcc = geom->GetVolume("volAcceleratorDisk");
    volAcc->SetLineColor(kBlue);
    volAcc->SetTransparency(0);

    TGeoVolume *volAanode = geom->GetVolume("volAnodeDisk");
    volAanode->SetLineColor(kYellow);
    volAanode->SetTransparency(0);

    gGeoManager->GetTopNode();
    gGeoManager->SetMaxVisNodes(70000);
    gGeoManager->FindVolumeFast("volWorld")->Draw("ogl");

}